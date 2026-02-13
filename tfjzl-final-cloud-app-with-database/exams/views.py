
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from .models import Course, Question, Choice, Submission

def course_detail(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related('questions__choices'),
        pk=course_id
    )
    return render(request, 'exams/course_detail.html', {'course': course})


@require_http_methods(["POST"])
def submit_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.create(
        course=course,
        user=request.user if request.user.is_authenticated else None
    )

    for question in course.questions.all():
        field_name = f"choice_{question.id}"
        values = request.POST.getlist(field_name)
        if not values:
            continue
        valid_choices = Choice.objects.filter(question=question, id__in=values)
        submission.selected_choices.add(*valid_choices)

    submission.evaluate()
    submission.save()

    return redirect('exams:exam_result', submission_id=submission.id)


def exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related('course', 'user').prefetch_related('selected_choices__question__choices'),
        pk=submission_id
    )

    course = submission.course

    per_question = []
    selected_by_q = {}
    for choice in submission.selected_choices.all():
        selected_by_q.setdefault(choice.question_id, set()).add(choice.id)

    for q in course.questions.all().prefetch_related('choices'):
        correct_ids = {c.id for c in q.choices.all() if c.is_correct}
        picked_ids = selected_by_q.get(q.id, set())
        is_correct = (picked_ids == correct_ids)
        per_question.append({
            'question': q,
            'choices': q.choices.all(),
            'picked_ids': picked_ids,
            'correct_ids': correct_ids,
            'is_correct': is_correct,
        })

    context = {
        'submission': submission,
        'course': course,
        'per_question': per_question,
    }
    return render(request, 'exams/exam_result.html', context)
