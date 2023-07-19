from django.urls import resolve, reverse
from django.test import SimpleTestCase

from notifications.views import (
    UnreadNotificationCountAPIView,
    NotificationsAPIView,
    RemoveNotificationAPIView,
)


class NotificationsUrlsTests(SimpleTestCase):

    def test_notifications_api_view_is_resolved(self):
        """Test that NotificationsAPIView url works correctly."""
        url = reverse('notifications')
        self.assertEquals(
            resolve(url).func.view_class, NotificationsAPIView,
        )

    def test_unread_count_api_view_is_resolved(self):
        """Test that UnreadNotificationCountAPIView url works correctly."""
        url = reverse('unread_count')
        self.assertEquals(
            resolve(url).func.view_class, UnreadNotificationCountAPIView,
        )

    def test_remove_notification_api_view_is_resolved(self):
        """Test that RemoveNotificationAPIView url works correctly."""
        url = reverse('remove_notification', args=[1, ])
        self.assertEquals(
            resolve(url).func.view_class, RemoveNotificationAPIView,
        )
