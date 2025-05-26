from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Basic extra fields
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # Social & organization
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    organization = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, blank=True)
    # Permissions or extra flags
    is_verified = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=True)
    # Add more fields as needed to accomplish your mission

    def __str__(self):
        return self.username
