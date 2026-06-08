from django.contrib import admin
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ["name", "description"]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ["content", "course", "grade"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "date_enrolled"]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["enrollment", "submitted_at", "get_score"]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)