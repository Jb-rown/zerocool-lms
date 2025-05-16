from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson
from .forms import CourseForm, LessonForm

@login_required
def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = request.user in course.students.all()
    return render(request, 'courses/detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_student:
        course.students.add(request.user)
        return redirect('course_detail', pk=pk)
    return redirect('course_list')