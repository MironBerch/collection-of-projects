from django.test import TestCase

from core.testing import create_post
from accounts.models import User
from accounts.services import follow_user
from posts.models import Post


class PostManagerTestCase(TestCase):
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

    def test_active(self):
        create_post(self.user1)
        p2 = create_post(self.user1)
        p2.is_active = False
        p2.save()
        active_posts = Post.objects.active()
        self.assertEqual(active_posts.count(), 1)

    def test_feed(self):
        create_post(self.user1)
        create_post(self.user2)
        create_post(self.user3)
        follow_user(
            self=self.user1,
            user=self.user2,
        )
        feed_count = (
            Post.objects.feed(
                self.user1
            ).count()
        )
        self.assertEqual(feed_count, 2)

    def test_posts(self):
        p1 = create_post(self.user1)
        create_post(
            self.user1,
            is_reply=True,
            parent=p1,
        )

        p2 = create_post(self.user1)
        p2.is_active = False
        p2.save()

        posts = (
            Post.objects.posts()
            .filter(
                author=self.user1
            )
        )

        post_count = posts.count()
        self.assertEqual(post_count, 1)

        reply_count = len(posts[0].reply_ids)
        self.assertEqual(reply_count, 1)

        create_post(self.user1, parent=p1)
        repost_count = len(posts[0].repost_ids)
        self.assertEqual(repost_count, 1)

    def test_profile_posts(self):
        create_post(self.user1)

        p2 = create_post(self.user1)
        p2.is_active = False
        p2.save()

        create_post(self.user2)

        profile_post_count = (
            Post.objects.profile_posts(
                self.user1,
            ).count()
        )
        self.assertEqual(profile_post_count, 1)

    def test_recommend_posts(self):
        p1 = create_post(self.user2)
        create_post(self.user3, parent=p1)
        create_post(self.user3)
        follow_user(
            self=self.user1,
            user=self.user2,
        )
        recommend_post_count = (
            Post.objects.recommend_posts(
                self.user1
            ).count()
        )
        self.assertEqual(recommend_post_count, 1)

        for _ in range(0, 10):
            create_post(self.user3)

        recommend_post_count = (
            Post.objects.recommend_posts(
                self.user1
            ).count()
        )
        self.assertEqual(recommend_post_count, 5)

        recommend_post_count = (
            Post.objects.recommend_posts(
                self.user1,
                long=True,
            ).count()
        )
        self.assertEqual(recommend_post_count, 11)
