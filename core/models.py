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
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TeamMembership',
        related_name='teams'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('mentor', 'Mentor'),
        # add more as needed
    ]
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.role})"

class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='projects')
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_projects',
        help_text="Project leader (optional)"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projects'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    category = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField('ProjectTag', blank=True, related_name='projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('done', 'Done'),
        ('blocked', 'Blocked'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('TaskTag', blank=True, related_name='tasks')

    def __str__(self):
        return self.title

class TaskTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class TaskComment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskAttachment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TaskTimeLog(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration(self):
        return self.end_time - self.start_time

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('task_assigned', 'Task Assigned'),
        ('task_status_changed', 'Task Status Changed'),
        ('task_commented', 'Task Commented'),
        ('project_updated', 'Project Updated'),
        ('general', 'General'),
        # Add more as needed
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    url = models.URLField(blank=True, null=True, help_text='Optional link to the relevant resource')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: For linking directly to related objects (advanced)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"

