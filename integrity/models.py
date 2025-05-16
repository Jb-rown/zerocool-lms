from django.db import models
from assignments.models import Submission
from django.conf import settings

class PlagiarismCheck(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
    similarity_score = models.FloatField()
    report = models.JSONField()  # Stores detailed plagiarism report
    
    class Meta:
        verbose_name_plural = "Plagiarism Checks"
    
    def __str__(self):
        return f"Plagiarism check for {self.submission}"

class ExamProctoringSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    video_recording = models.FileField(upload_to='proctoring/', blank=True)
    flags = models.JSONField(default=list)  # Stores suspicious activity flags
    
    def __str__(self):
        return f"Proctoring session for {self.user} on {self.exam}"