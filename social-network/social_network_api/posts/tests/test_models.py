from django.test import TestCase

from core.testing import create_post
from accounts.models import User


class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            email='user1@gmail.com',
            username='Miron1',
            first_name='John',
            last_name='Doe',
            password='password',
        )

    def test_string_representation(self):
        p = create_post(self.user1)
        self.assertEqual(str(p), 'content')

    def test_get_replies(self):
        p = create_post(self.user1)
        create_post(self.user1, is_reply=True, parent=p)

        r2 = create_post(self.user1, is_reply=True, parent=p)
        r2.is_active = False
        r2.save()

        reply_count = p.get_replies().count()
        self.assertEqual(reply_count, 1)

    def test_get_reposts(self):
        p = create_post(self.user1)
        create_post(self.user1, is_reply=True, parent=p)
        create_post(self.user1, is_reply=False, parent=p)

        rp2 = create_post(self.user1, is_reply=False, parent=p)
        rp2.is_active = False
        rp2.save()

        repost_count = p.get_reposts().count()
        self.assertEqual(repost_count, 1)
