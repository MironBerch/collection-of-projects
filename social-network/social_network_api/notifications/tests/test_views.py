from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from posts.models import Post
from accounts.models import User


class NotificationMixin:
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user@gmail.com',
            username='JohnDoe',
            first_name='John',
            last_name='Doe',
            password='password',
        )
        self.user2 = User.objects.create_user(
            email='user2@gmail.com',
            username='JohnDoe2',
            first_name='John2',
            last_name='Doe2',
            password='password',
        )

    def create_notification(self):
        post_url = reverse('post')

        self.client.force_authenticate(user=self.user1)
        post_data = {
            'content': 'testing',
            'is_reply': False,
        }
        self.client.post(post_url, post_data)

        self.client.force_authenticate(user=self.user2)
        p = Post.objects.get(content='testing')
        reply_data = {
            'content': 'testing',
            'is_reply': True,
            'parent_id': p.id,
        }
        self.client.post(post_url, reply_data)

        self.client.force_authenticate(user=self.user1)


class UnreadNotificationCountViewTestCase(NotificationMixin, APITestCase):
    url = reverse('unread_count')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unread_notification_count(self):
        self.create_notification()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, 1)


class NoticationsViewTestCase(NotificationMixin, APITestCase):
    url = reverse('notifications')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notifications(self):
        self.create_notification()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        notification_count = len(response.data.get('results'))
        self.assertEqual(notification_count, 1)


class RemoveNotificationTestCase(NotificationMixin, APITestCase):
    endpoint = 'remove_notification'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_notification(self):
        self.create_notification()
        notification = self.user1.notifications.first()
        url = reverse(self.endpoint, kwargs={'pk': notification.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        notification_count = self.user1.notifications.count()
        self.assertEqual(notification_count, 0)
