from django.contrib.auth import authenticate
from django.test import TestCase

from accounts.models import User


class AuthenticateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='email@gmail.com',
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )

    def test_authenticate_with_no_credentials(self):
        """
        Check that `None` is returned if no credentials are provided.
        """
        a = authenticate()
        self.assertIsNone(a)

    def test_authenticate_with_bad_credentials(self):
        """
        Check that `None` is returned if bad credentials are provided.
        """
        a = authenticate(email='bad-username', password='bad-password')
        self.assertIsNone(a)

    def test_authenticate_with_email(self):
        """
        Check that user can authenticate with their email address.
        """
        a = authenticate(email='email@gmail.com', password='password')
        self.assertIsNotNone(a)

    def test_authenticate_with_username(self):
        """
        Check that user can authenticate with their username.
        """
        a = authenticate(email='username', password='password')
        self.assertIsNotNone(a)

    def test_authenticate_with_email_with_caps(self):
        """
        Check that user can authenticate with their email
        address, disregarding case sensitivity.
        """
        a = authenticate(email='JIM@TESTING.COM', password='password')
        self.assertIsNone(a)

    def test_authenticate_with_username_with_caps(self):
        """
        Check that user can not authenticate with their username,
        disregarding case sensitivity.
        """
        a = authenticate(login='JIM', password='password')
        self.assertIsNone(a)
