from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_notification_creation(self):
        notif = Notification.objects.create(
            user=self.user,
            notification_type='general',
            message='Test notification'
        )
        self.assertEqual(notif.user, self.user)
        self.assertEqual(notif.notification_type, 'general')
        self.assertFalse(notif.is_read)