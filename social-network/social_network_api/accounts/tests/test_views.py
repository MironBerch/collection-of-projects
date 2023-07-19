from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class SignupAPIViewTests(APITestCase):
    url = reverse('signup')

    def test_signup(self):
        """Test that SignupAPIView works correctly."""
        data = {
            'email': 'email@gmail.com',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': 'password',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class SigninAPIViewTests(APITestCase):
    url = reverse('signin')

    def setUp(self):
        User.objects.create_user(
            email='user@gmail.com',
            username='JohnDoe',
            first_name='John',
            last_name='Doe',
            password='password',
        )

    def test_signin_with_success_status_code(self):
        """Test that signin works with corect credentials."""
        credentials = {
            'email': 'user@gmail.com',
            'password': 'password',
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_with_failure_status_code(self):
        """Test that signin works with uncorect credentials."""
        credentials = {
            'email': 'not@gmail.com',
            'password': 'password',
        }
        response = self.client.post(self.url, credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SignoutAPIViewTests(APITestCase):
    url = reverse('signout')

    def test_signout_status_code(self):
        """Test that SignoutAPIView return correct status code."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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

    def authenticate(self):
        self.client.force_authenticate(user=self.user1)


class UserDetailViewTestCase(Mixin, APITestCase):
    def test_unauthorized_status_code(self):
        url = reverse('user_detail', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_status_code(self):
        self.authenticate()
        url = reverse('user_detail', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_username_does_not_exist(self):
        self.authenticate()
        url = reverse('user_detail', kwargs={'username': 'bad-username'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EditProfileViewTestCase(Mixin, APITestCase):
    url = reverse('edit_profile')

    def test_unauthorized_status_code(self):
        response = self.client.patch(self.url, {'website': 'testing.com'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_profile(self):
        self.authenticate()
        response = self.client.patch(self.url, {'description': 'testing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.user1.profile.description, 'testing')


class EditUserViewTestCase(Mixin, APITestCase):
    url = reverse('edit_user')

    def test_unauthorized_status_code(self):
        response = self.client.patch(self.url, {'first_name': self.user1.first_name})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_status_code(self):
        self.authenticate()
        response = self.client.patch(self.url, {'first_name': 'new-first-name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.user1.first_name, 'new-first-name')


class EditPasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@gmail.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='oldpassword',
        )
        self.url = reverse('edit_password')

    def test_password_update_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'current_password': 'oldpassword',
            'password': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        self.assertEqual(response.data['message'], 'Password updated successfully.')

    def test_password_update_invalid_current_password(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'current_password': 'wrongpassword',
            'password': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid current password.')

    def test_password_update_mismatched_passwords(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'current_password': 'oldpassword',
            'password': 'newpassword123',
            'password2': 'differentpassword',
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'New passwords do not match.')


class FollowingViewTestCase(Mixin, APITestCase):
    def test_unauthorized_status_code(self):
        url = reverse('following', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_username_does_not_exist(self):
        self.authenticate()
        url = reverse('following', kwargs={'username': 'bad-username'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_following(self):
        self.authenticate()
        url = reverse('following', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure the response data is paginated.
        self.assertIsInstance(response.data.get('results'), list)

    def test_follow(self):
        self.authenticate()
        url = reverse('following', kwargs={'username': self.user2.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        following_count = self.user1.following.count()
        self.assertEqual(following_count, 1)

        notification_count = self.user2.notifications.count()
        self.assertEqual(notification_count, 1)

    def test_unfollow(self):
        self.authenticate()
        url = reverse('following', kwargs={'username': self.user2.username})

        self.client.post(url)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        following_count = self.user1.following.count()
        self.assertEqual(following_count, 0)

        notification_count = self.user2.notifications.count()
        self.assertEqual(notification_count, 0)


class FollowersViewTestCase(Mixin, APITestCase):
    def test_unauthorized_status_code(self):
        url = reverse('followers', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_followers(self):
        self.authenticate()
        url = reverse('followers', kwargs={'username': self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

    def test_username_does_not_exist(self):
        self.authenticate()
        url = reverse('followers', kwargs={'username': 'bad-username'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RecommendedUsersViewTestCase(Mixin, APITestCase):
    url = reverse('recommended_users')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recommeneded_users(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recommended_user = response.data[0].get('username')
        self.assertEqual(recommended_user, self.user2.username)


class LongRecommendedUsersViewTestCase(Mixin, APITestCase):
    url = reverse('long_recommended_users')

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_long_recommended_users(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data.get('results'), list)

        recommended_user = response.data.get('results')[0].get('username')
        self.assertEqual(recommended_user, self.user2.username)
