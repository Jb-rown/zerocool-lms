from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_researcher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    points = models.IntegerField(default=0)
    house = models.CharField(max_length=50, blank=True)  # For gamification
    
    def __str__(self):
        return self.username