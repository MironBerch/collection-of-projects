from django.test import TestCase

from accounts.models import User, Profile


class AccountsSignalsTests(TestCase):

    def setUp(self) -> None:
        User.objects.create_user(
            email='user@gmail.com',
            username='JohnDoe',
            first_name='John',
            last_name='Doe',
            password='password',
        )
        User.objects.create_superuser(
            email='superuser@gmail.com',
            username='BillWhite',
            first_name='Bill',
            last_name='White',
            password='password',
        )

    def test_create_user_profile_signal(self):
        """Test that create_user_profile signal works with new users."""
        self.assertTrue(Profile.objects.get(user=User.objects.get(email='user@gmail.com')))

    def test_create_superuser_profile_signal(self):
        """Test that create_user_profile signal works with new superusers."""
        self.assertTrue(Profile.objects.get(user=User.objects.get(email='superuser@gmail.com')))
