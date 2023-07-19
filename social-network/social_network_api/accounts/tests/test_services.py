from django.test import TestCase

from accounts.models import User
from accounts.services import (
    get_user_profile,
    get_user_by_username,
    follow_user,
    get_followers,
    get_following,
    unfollow,
)


class AccountsServicesTests(TestCase):

    def setUp(self):
        User.objects.create_user(
            email='user@gmail.com',
            username='JohnDoe',
            first_name='John',
            last_name='Doe',
            password='password',
        )

    def test_get_user_profile(self):
        """Test that get_user_profile method works correctly."""
        self.assertTrue(
            User.objects.get(email='user@gmail.com'),
            get_user_profile(user=User.objects.get(email='user@gmail.com')),
        )

    def test_get_user_by_username(self):
        """Test that get_user_by_username method works correctly."""
        self.assertTrue(
            User.objects.get(email='user@gmail.com'),
            get_user_by_username(username='JohnDoe'),
        )


class Mixin:
    @classmethod
    def setUp(cls):
        cls.user1 = User.objects.create_user(
            email='user@gmail.com',
            username='JohnDoe',
            first_name='John',
            last_name='Doe',
            password='password',
        )

        cls.user2 = User.objects.create_user(
            email='user2@gmail.com',
            username='JohnDoe2',
            first_name='John2',
            last_name='Doe2',
            password='password',
        )


class UserModelTestCase(Mixin, TestCase):
    def test_follow(self):
        follow_user(self=self.user1, user=self.user2)
        self.assertEqual(self.user1.following.count(), 1)

    def test_get_followers(self):
        follow_user(self=self.user2, user=self.user1)
        followers_count = get_followers(self.user1).count()
        self.assertEqual(followers_count, 1)

    def test_get_following(self):
        follow_user(self=self.user1, user=self.user2)
        following_count = get_following(self.user1).count()
        self.assertEqual(following_count, 1)

    def test_unfollow(self):
        follow_user(self=self.user1, user=self.user2)
        unfollow(self=self.user1, user=self.user2)
        following_count = get_following(self.user1).count()
        self.assertEqual(following_count, 0)
