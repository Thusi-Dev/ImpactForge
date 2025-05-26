from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # Inherit all fields from AbstractUser (username, email, password, etc.)
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    organization = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
