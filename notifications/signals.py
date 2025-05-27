from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Task, TaskComment
from .services import notify_task_assigned, notify_task_status_changed, notify_task_commented

# Notify assignee when a task is created or reassigned
@receiver(post_save, sender=Task)
def task_assignment_signal(sender, instance, created, **kwargs):
    if created and instance.assignee:
        notify_task_assigned(user=instance.assignee, task=instance)
    else:
        # Logic for reassignment: you might want to compare previous assignee with the new one.
        # For simplicity, this example notifies on every save if there's an assignee.
        # For production: check if assignee changed before notifying.
        pass

# Notify assignee when a task status changes
@receiver(post_save, sender=Task)
def task_status_change_signal(sender, instance, created, **kwargs):
    if not created and instance.assignee:
        # You would want to compare previous status with current status.
        # This requires custom logic, perhaps with a pre_save signal or by tracking status before save.
        # Example placeholder:
        # if instance.status != instance._old_status:
        #     notify_task_status_changed(user=instance.assignee, task=instance, old_status=instance._old_status, new_status=instance.status)
        pass

# Notify assignee when a new comment is added to their task
@receiver(post_save, sender=TaskComment)
def task_commented_signal(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        if task.assignee and instance.author != task.assignee:
            notify_task_commented(user=task.assignee, task=task, comment=instance)