from django.urls import resolve, reverse
from django.test import SimpleTestCase

from accounts.views import (
    SignupAPIView,
    SigninAPIView,
    SignoutAPIView,
    EditPasswordAPIView,
    EditProfileAPIView,
    EditUserAPIView,
    FollowersAPIView,
    FollowingAPIView,
    LongRecommendedUsersAPIView,
    RecommendedUsersAPIView,
    UserDetailAPIView,
)


class AccountsUrlsTests(SimpleTestCase):

    def test_signup_api_view_is_resolved(self):
        """Test that SignupAPIView url works correctly."""
        url = reverse('signup')
        self.assertEquals(
            resolve(url).func.view_class, SignupAPIView,
        )

    def test_signin_api_view_is_resolved(self):
        """Test that SigninAPIView url works correctly."""
        url = reverse('signin')
        self.assertEquals(
            resolve(url).func.view_class, SigninAPIView,
        )

    def test_signout_api_view_is_resolved(self):
        """Test that SignoutAPIView url works correctly."""
        url = reverse('signout')
        self.assertEquals(
            resolve(url).func.view_class, SignoutAPIView,
        )

    def test_edit_password_api_view_is_resolved(self):
        """Test that EditPasswordAPIView url works correctly."""
        url = reverse('edit_password')
        self.assertEquals(
            resolve(url).func.view_class, EditPasswordAPIView,
        )

    def test_edit_profile_api_view_is_resolved(self):
        """Test that EditProfileAPIView url works correctly."""
        url = reverse('edit_profile')
        self.assertEquals(
            resolve(url).func.view_class, EditProfileAPIView,
        )

    def test_edit_user_api_view_is_resolved(self):
        """Test that EditUserAPIView url works correctly."""
        url = reverse('edit_user')
        self.assertEquals(
            resolve(url).func.view_class, EditUserAPIView,
        )

    def test_long_recommended_users_api_view_is_resolved(self):
        """Test that LongRecommendedUsersAPIView url works correctly."""
        url = reverse('long_recommended_users')
        self.assertEquals(
            resolve(url).func.view_class, LongRecommendedUsersAPIView,
        )

    def test_recommended_users_api_view_is_resolved(self):
        """Test that RecommendedUsersAPIView url works correctly."""
        url = reverse('recommended_users')
        self.assertEquals(
            resolve(url).func.view_class, RecommendedUsersAPIView,
        )

    def test_user_detail_api_view_is_resolved(self):
        """Test that UserDetailAPIView url works correctly."""
        url = reverse('user_detail', args=['username', ])
        self.assertEquals(
            resolve(url).func.view_class, UserDetailAPIView,
        )

    def test_following_api_view_is_resolved(self):
        """Test that FollowingAPIView url works correctly."""
        url = reverse('following', args=['username', ])
        self.assertEquals(
            resolve(url).func.view_class, FollowingAPIView,
        )

    def test_followers_api_view_is_resolved(self):
        """Test that FollowersAPIView url works correctly."""
        url = reverse('followers', args=['username', ])
        self.assertEquals(
            resolve(url).func.view_class, FollowersAPIView,
        )
