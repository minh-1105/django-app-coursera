from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Choice, Submission


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    if enrollment is None:
        enrollment = Enrollment.objects.create(
            user=request.user,
            course=course
        )

    if request.method == "POST":
        selected_choice_ids = request.POST.getlist("choice")

        submission = Submission.objects.create(
            enrollment=enrollment
        )

        selected_choices = Choice.objects.filter(
            id__in=selected_choice_ids
        )

        submission.choices.set(selected_choices)
        submission.save()

        return redirect(
            "onlinecourse:show_exam_result",
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect("onlinecourse:course_details", course_id=course.id)


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choices = submission.choices.all()
    total_score = 0

    for question in course.question_set.all():
        total_score += question.grade

    score = submission.get_score()

    if total_score > 0:
        grade = round((score / total_score) * 100, 2)
    else:
        grade = 0

    context = {
        "course": course,
        "submission": submission,
        "selected_choices": selected_choices,
        "score": score,
        "total_score": total_score,
        "grade": grade,
    }

    return render(request, "onlinecourse/exam_result_bootstrap.html", context)