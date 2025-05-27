from django.urls import reverse
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

def create_notification(
    user,
    notification_type,
    message,
    url=None,
    related_object=None,
    priority='',
    delivered=False
):
    """
    General-purpose function to create a notification.
    """
    content_type = None
    object_id = None
    if related_object:
        content_type = ContentType.objects.get_for_model(related_object)
        object_id = related_object.pk
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        url=url,
        content_type=content_type,
        object_id=object_id,
        priority=priority,
        delivered=delivered
    )

# --- Specific Notification Helpers ---

def notify_task_assigned(user, task, assigner=None):
    message = f"You have been assigned to the task: {task.title}"
    if assigner and assigner != user:
        message += f" (assigned by {assigner.get_full_name() or assigner.username})"
    url = reverse('task_detail', args=[task.id])
    return create_notification(
        user=user,
        notification_type='task_assigned',
        message=message,
        url=url,
        related_object=task
    )

def notify_task_status_changed(user, task, old_status, new_status):
    message = f"Task '{task.title}' status changed from {old_status} to {new_status}."
    url = reverse('task_detail', args=[task.id])
    return create_notification(
        user=user,
        notification_type='task_status_changed',
        message=message,
        url=url,
        related_object=task
    )

def notify_task_commented(user, task, comment):
    message = f"New comment on task '{task.title}': {comment.content[:50]}"
    url = reverse('task_detail', args=[task.id])
    return create_notification(
        user=user,
        notification_type='task_commented',
        message=message,
        url=url,
        related_object=comment
    )

def notify_project_updated(user, project, update_message):
    message = f"Project '{project.name}' updated: {update_message}"
    url = reverse('project_detail', args=[project.id])
    return create_notification(
        user=user,
        notification_type='project_updated',
        message=message,
        url=url,
        related_object=project
    )

# --- Bulk/Group Notifications ---

def notify_multiple_users(users, notification_type, message, url=None, related_object=None):
    notifications = []
    for user in users:
        notifications.append(
            create_notification(
                user=user,
                notification_type=notification_type,
                message=message,
                url=url,
                related_object=related_object
            )
        )
    return notifications

# --- Mark as Read/Unread Utilities ---

def mark_notification_as_read(notification):
    notification.is_read = True
    notification.save(update_fields=['is_read'])

def mark_all_as_read(user):
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)

def mark_notification_as_unread(notification):
    notification.is_read = False
    notification.save(update_fields=['is_read'])

# --- Query Utilities ---

def get_unread_notifications(user):
    return Notification.objects.filter(user=user, is_read=False).order_by('-created_at')

def get_recent_notifications(user, limit=20):
    return Notification.objects.filter(user=user).order_by('-created_at')[:limit]