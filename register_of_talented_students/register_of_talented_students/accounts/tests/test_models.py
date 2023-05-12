from django.test import TestCase

from accounts.models import User


class TestUserModels(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='user@gmail.com',
            name='name',
            surname='surname',
            password='password',
        )
        self.admin = User.objects.create_superuser(
            email='admin@gmail.com',
            name='name',
            surname='surname',
            password='password',
        )

    def test_default_user_parameters(self):
        """Test default user parameters"""
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_verified)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_default_admin_parameters(self):
        """Test default admin parameters"""
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_verified)
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)
