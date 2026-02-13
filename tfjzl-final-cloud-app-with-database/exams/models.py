
from django.conf import settings
from django.db import models

# Mini-Fallback, NUR verwenden, wenn du kein eigenes Course-Modell hast
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    grade = models.PositiveIntegerField(default=1)
    allow_multiple = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"[{self.course}] {self.text[:60]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        prefix = "✓" if self.is_correct else "✗"
        return f"{prefix} {self.text[:60]}"


class Submission(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='exam_submissions'
    )
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)

    def __str__(self):
        uname = self.user.username if self.user else "anonym"
        return f"Submission({uname} -> {self.course}) @ {self.submitted_at:%Y-%m-%d %H:%M:%S}"

    def evaluate(self):
        total = 0
        for q in self.course.questions.all():
            total += q.grade

        score = 0
        selected_by_q = {}
        for choice in self.selected_choices.all().select_related('question'):
            selected_by_q.setdefault(choice.question_id, set()).add(choice.id)

        for q in self.course.questions.prefetch_related('choices'):
            correct_ids = {c.id for c in q.choices.all() if c.is_correct}
            picked_ids = selected_by_q.get(q.id, set())
            if picked_ids == correct_ids:
                score += q.grade

        self.max_score = total
        self.score = score
        self.passed = (self.max_score > 0 and self.score / self.max_score >= 0.6)
        return self.score, self.max_score, self.passed
