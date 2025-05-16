from django.db import models
from accounts.models import User
from courses.models import Course

class ResearchProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervised_projects')
    students = models.ManyToManyField(User, related_name='research_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class LibraryResource(models.Model):
    RESOURCE_TYPES = (
        ('book', 'Book'),
        ('paper', 'Research Paper'),
        ('video', 'Video Lecture'),
        ('dataset', 'Dataset'),
    )
    
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='library/')
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_resource_type_display()}: {self.title}"