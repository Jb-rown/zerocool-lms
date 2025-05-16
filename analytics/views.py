from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course, Lesson
from assignments.models import Submission
import plotly.express as px
from plotly.offline import plot

@login_required
def learning_analytics(request):
    # Course progress data
    enrolled_courses = request.user.courses_enrolled.all()
    course_progress = []
    
    for course in enrolled_courses:
        total_lessons = course.lesson_set.count()
        completed_lessons = course.lesson_set.filter(
            completions__user=request.user
        ).count()
        progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        course_progress.append({
            'course': course.title,
            'progress': progress
        })
    
    # Create progress chart
    progress_fig = px.bar(
        course_progress,
        x='course',
        y='progress',
        title='Your Course Progress',
        labels={'progress': 'Progress (%)', 'course': 'Course'},
        color='progress',
        color_continuous_scale='Viridis'
    )
    progress_plot = plot(progress_fig, output_type='div')
    
    # Grade distribution
    submissions = Submission.objects.filter(student=request.user).exclude(grade__isnull=True)
    if submissions.exists():
        grades_fig = px.histogram(
            x=[s.grade for s in submissions],
            title='Your Grade Distribution',
            labels={'x': 'Grade'},
            nbins=10
        )
        grades_plot = plot(grades_fig, output_type='div')
    else:
        grades_plot = None
    
    return render(request, 'analytics/dashboard.html', {
        'progress_plot': progress_plot,
        'grades_plot': grades_plot
    })