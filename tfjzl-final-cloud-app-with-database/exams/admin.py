from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission
)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_time', 'total_learners')

@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ('occupation', 'social_link')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'is_correct', 'question')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'submitted_at')
