from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from accounts.models import User


class SearchViewTestCase(APITestCase):
    url = reverse('search')

    def setUp(self):
        User.objects.create_user(
            email='user@gmail.com',
            username='Miron',
            first_name='John',
            last_name='Doe',
            password='password',
        )

    def test_unauthorized_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search(self):
        """
        Test correctly search with username, first_name and last_name fields.
        """

        self.client.force_authenticate(
            user=User.objects.get(email='user@gmail.com'),
        )

        response1 = self.client.get(f'{self.url}?search=Miron')
        response2 = self.client.get(f'{self.url}?search=John')
        response3 = self.client.get(f'{self.url}?search=Doe')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

        results_count1 = len(response1.data.get('results'))
        results_count2 = len(response2.data.get('results'))
        results_count3 = len(response3.data.get('results'))

        self.assertEqual(results_count1, 1)
        self.assertEqual(results_count2, 1)
        self.assertEqual(results_count3, 1)
