
from django.contrib import admin
from .models import Course, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'grade', 'allow_multiple', 'order')
    list_filter = ('course', 'allow_multiple')
    search_fields = ('text',)
    inlines = [ChoiceInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_filter = ('published',)
    search_fields = ('title',)
    inlines = [QuestionInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'submitted_at', 'score', 'max_score', 'passed')
    list_filter = ('course', 'passed')
    search_fields = ('user__username', 'course__title')
    filter_horizontal = ('selected_choices',)
