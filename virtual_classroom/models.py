from django.db import models
from courses.models import Course
from accounts.models import User

class VirtualClass(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    meeting_id = models.CharField(max_length=100)
    meeting_password = models.CharField(max_length=50, blank=True)
    schedule = models.JSONField()  # Stores recurring schedule
    
    def __str__(self):
        return f"Virtual Class: {self.course.title}"

class ClassRecording(models.Model):
    virtual_class = models.ForeignKey(VirtualClass, on_delete=models.CASCADE)
    recording_url = models.URLField()
    recording_date = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    
    def __str__(self):
        return f"Recording from {self.recording_date}"