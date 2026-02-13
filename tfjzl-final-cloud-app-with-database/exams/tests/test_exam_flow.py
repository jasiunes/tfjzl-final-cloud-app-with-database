
from django.test import TestCase
from django.urls import reverse
from exams.models import Course, Question, Choice

class ExamFlowTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Demo", description="Testkurs")
        q1 = Question.objects.create(course=self.course, text="2+2?", grade=2, allow_multiple=False, order=1)
        self.c1 = Choice.objects.create(question=q1, text="4", is_correct=True)
        self.c2 = Choice.objects.create(question=q1, text="5", is_correct=False)

    def test_submit_and_result(self):
        url_submit = reverse('exams:submit_exam', args=[self.course.id])
        resp = self.client.post(url_submit, data={f"choice_{self.c1.question.id}": str(self.c1.id)})
        self.assertEqual(resp.status_code, 302)
