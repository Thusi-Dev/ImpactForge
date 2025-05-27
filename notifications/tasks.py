from celery import shared_task
from .models import Notification, Device
from pyfcm import FCMNotification
from django.conf import settings

@shared_task
def send_push_notification(notification_id):
    """
    Send a push notification to all of the user's devices for a notification.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        user = notification.user
        devices = user.devices.all()
        if not devices:
            return

        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        message_title = "New Notification"
        message_body = notification.message

        registration_ids = [device.registration_id for device in devices]
        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body,
            data_message={"url": notification.url}
        )
        notification.delivered = True
        notification.save(update_fields=['delivered'])
        return result
    except Notification.DoesNotExist:
        pass

from django.core.mail import send_mail

@shared_task
def send_notification_email(notification_id):
    """
    Send an email to the user for a specific notification.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.user.email:
            send_mail(
                subject=f"Notification: {notification.get_notification_type_display()}",
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=True,
            )
            notification.delivered = True
            notification.save(update_fields=['delivered'])
    except Notification.DoesNotExist:
        pass

@shared_task
def send_bulk_notification_emails(notification_ids):
    """
    Send emails for a list of notification IDs.
    """
    for nid in notification_ids:
        send_notification_email.delay(nid)