from django.test import TestCase, Client
from django.urls import reverse


class TestSignupView(TestCase):

    def test_signup_view_get_method(self):
        client = Client()
        response = client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')


class TestSigninView(TestCase):

    def test_signin_view_get_method(self):
        client = Client()
        response = client.get(reverse('signin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signin.html')
