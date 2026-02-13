
from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/submit/', views.submit_exam, name='submit_exam'),
    path('submissions/<int:submission_id>/result/', views.exam_result, name='exam_result'),
]
