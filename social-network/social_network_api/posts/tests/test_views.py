from rest_framework import status
from rest_framework.test import APITestCase

from django.db.models import Q
from django.urls import reverse

from core.testing import create_post
from accounts.models import User
from accounts.services import follow_user


class Mixin:
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            email='user1@gmail.com',
            username='Miron1',
            first_name='John',
            last_name='Doe',
            password='password',
        )
        cls.user2 = User.objects.create_user(
            email='user2@gmail.com',
            username='Miron2',
            first_name='John',
            last_name='Doe',
            password='password',
        )
        cls.user3 = User.objects.create_user(
            email='user3@gmail.com',
            username='Miron3',
            first_name='John',
            last_name='Doe',
            password='password',
        )


class BadPKMixin:
    endpoint = None

    def test_pk_does_not_exist(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(self.endpoint, kwargs={'pk': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BadSlugMixin:
    endpoint = None

    def test_slug_does_not_exist(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(self.endpoint, kwargs={'username': 'bad-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FeedViewTestCase(Mixin, APITestCase):
    url = reverse('feed')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed(self):
        self.client.force_authenticate(user=self.user1)
        create_post(self.user1)
        create_post(self.user2)
        create_post(self.user3)
        follow_user(self=self.user1, user=self.user2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        results_count = len(response.data.get('results'))
        self.assertEqual(results_count, 2)


class ProfilePostsViewTestCase(Mixin, BadSlugMixin, APITestCase):
    endpoint = 'profile_posts'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_posts(self):
        self.client.force_authenticate(user=self.user1)
        create_post(self.user1)
        create_post(self.user2)
        url = reverse(self.endpoint, kwargs={'username': self.user1.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        results_count = len(response.data.get('results'))
        self.assertEqual(results_count, 1)


class ProfileLikesViewTestCase(Mixin, BadSlugMixin, APITestCase):
    endpoint = 'profile_likes'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_likes(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(self.endpoint, kwargs={'username': self.user1.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        p = create_post(self.user1)
        p.liked.add(self.user1)
        post_likes_count = p.liked.count()
        self.assertEqual(post_likes_count, 1)


class PostViewTestCase(Mixin, APITestCase):
    url = reverse('post')

    def test_unauthorized_status_code(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'content': 'testing',
            'is_reply': False,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_count = self.user1.posts.filter(Q(parent_id=None), is_reply=False).count()
        self.assertEqual(post_count, 1)

    def test_create_reply(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user2)
        data = {
            'content': 'testing',
            'is_reply': True,
            'parent_id': p.id,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_count = self.user1.posts.filter(~Q(parent_id=None), is_reply=True).count()
        self.assertEqual(post_count, 1)

        notifications_count = self.user2.notifications.count()
        self.assertEqual(notifications_count, 1)


class RepostViewTestCase(Mixin, APITestCase):
    url = reverse('repost')

    def test_unauthorized_status_code(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_repost(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user2)
        data = {
            'content': 'testing',
            'is_reply': False,
            'parent_id': p.id,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        repost_count = p.alt.filter(~Q(parent_id=None), is_reply=False).count()
        self.assertEqual(repost_count, 1)

        notifications_count = self.user2.notifications.count()
        self.assertEqual(notifications_count, 1)


class PostDetailViewTestCase(Mixin, BadPKMixin, APITestCase):
    endpoint = 'post_detail'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_post_detail(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_must_be_owner(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user2)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        data = {'content': 'testing'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_detail(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        data = {'content': 'testing'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_content = self.user1.posts.get(pk=p.pk).content
        self.assertEqual(updated_content, 'testing')

    def test_delete_post_detail(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        post_count = self.user1.posts.active().count()
        self.assertEqual(post_count, 0)


class LikesViewTestCase(Mixin, BadPKMixin, APITestCase):
    endpoint = 'likes'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_likes(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        p.liked.add(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        likes_count = p.liked.count()
        self.assertEqual(likes_count, 1)

    def test_add_like(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        likes_count = p.liked.count()
        self.assertEqual(likes_count, 1)

    def test_delete_like(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        likes_count = p.liked.count()
        self.assertEqual(likes_count, 0)


class RecommendPostsViewTestCase(Mixin, APITestCase):
    url = reverse('recommended_posts')

    def test_unauthorized_status_code(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recommended_posts(self):
        self.client.force_authenticate(user=self.user1)
        create_post(self.user2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recommended_post_username = response.data[0].get('author').get('username')
        self.assertEqual(recommended_post_username, self.user2.username)


class LongRecommendedPostsViewTestCase(Mixin, APITestCase):
    url = reverse('long_recommended_posts')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_long_recommended_posts(self):
        self.client.force_authenticate(user=self.user1)
        create_post(self.user2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        recommended_post_username = (
            response.data.get('results')[0].get('author').get('username')
        )
        self.assertEqual(recommended_post_username, self.user2.username)


class PostRepliesTestCase(Mixin, BadPKMixin, APITestCase):
    endpoint = 'replies'

    def test_unauthorized_status_code(self):
        url = reverse(self.endpoint, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_post_replies(self):
        self.client.force_authenticate(user=self.user1)
        p = create_post(self.user1)
        create_post(self.user1, is_reply=True, parent=p)
        url = reverse(self.endpoint, kwargs={'pk': p.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        reply_count = p.get_replies().count()
        self.assertEqual(reply_count, 1)
