from django.urls import path
from . import views

urlpatterns = [
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('courses/<int:course_id>/submissions/<int:submission_id>/result/', 
         views.show_exam_result, 
         name='exam_result'),
]
