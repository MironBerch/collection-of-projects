from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import User


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email='email@gmail.com',
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )

        self.create_url = reverse('signup')

    def test_create_user(self):
        data = {
            'email': 'email2@gmail.com',
            'username': 'username2',
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'password': 'password2',
        }

        response = self.client.post(self.create_url, data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        data = {
            'email': 'email3@gmail.com',
            'username': 'username3',
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'password': 'pass',
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'email': 'email4@gmail.com',
            'username': 'username4',
            'first_name': 'first_name4',
            'last_name': 'last_name4',
            'password': '',
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)
