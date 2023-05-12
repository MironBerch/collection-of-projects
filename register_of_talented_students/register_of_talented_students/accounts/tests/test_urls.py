from django.urls import resolve, reverse
from django.test import SimpleTestCase

from accounts.views import SignupView, SigninView, SignoutView


class TestUserUrls(SimpleTestCase):

    def test_signup_view_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(
            resolve(url).func.view_class, SignupView,
        )

    def test_signin_view_is_resolved(self):
        url = reverse('signin')
        self.assertEquals(
            resolve(url).func.view_class, SigninView,
        )

    def test_signout_view_is_resolved(self):
        url = reverse('signout')
        self.assertEquals(
            resolve(url).func.view_class, SignoutView,
        )
