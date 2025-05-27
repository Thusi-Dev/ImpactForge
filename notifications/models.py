from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relationship to any object (e.g., Task, Project, Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Optional: notification priority, delivery status, etc.
    priority = models.CharField(max_length=10, blank=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Task, TaskComment
from .services import create_task_assigned_notification, create_comment_notification

@receiver(post_save, sender=Task)
def task_assignment_notification(sender, instance, created, **kwargs):
    if not created and instance.assignee:
        # Add additional logic to check if assignee changed
        create_task_assigned_notification(instance.assignee, instance)

@receiver(post_save, sender=TaskComment)
def comment_notification(sender, instance, created, **kwargs):
    if created and instance.task.assignee:
        create_comment_notification(instance.task.assignee, instance)