from django.urls import resolve, reverse
from django.test import SimpleTestCase

from posts.views import (
    PostAPIView,
    RepostAPIView,
    PostDetailAPIView,
    LikesAPIView,
    PostRepliesAPIView,
    FeedAPIView,
    ProfileLikesAPIView,
    ProfilePostsAPIView,
    LongRecommendedPostsAPIView,
    RecommendedPostsAPIView,
)


class PostsUrlsTests(SimpleTestCase):

    def test_post_api_view_is_resolved(self):
        """Test that PostAPIView url works correctly."""
        url = reverse('post')
        self.assertEquals(
            resolve(url).func.view_class, PostAPIView,
        )

    def test_repost_api_view_is_resolved(self):
        """Test that RepostAPIView url works correctly."""
        url = reverse('repost')
        self.assertEquals(
            resolve(url).func.view_class, RepostAPIView,
        )

    def test_post_detail_api_view_is_resolved(self):
        """Test that PostDetailAPIView url works correctly."""
        url = reverse('post_detail', args=[1, ])
        self.assertEquals(
            resolve(url).func.view_class, PostDetailAPIView,
        )

    def test_likes_api_view_is_resolved(self):
        """Test that LikesAPIView url works correctly."""
        url = reverse('likes', args=[1, ])
        self.assertEquals(
            resolve(url).func.view_class, LikesAPIView,
        )

    def test_replies_api_view_is_resolved(self):
        """Test that PostRepliesAPIView url works correctly."""
        url = reverse('replies', args=[1, ])
        self.assertEquals(
            resolve(url).func.view_class, PostRepliesAPIView,
        )

    def test_feed_api_view_is_resolved(self):
        """Test that FeedAPIView url works correctly."""
        url = reverse('feed')
        self.assertEquals(
            resolve(url).func.view_class, FeedAPIView,
        )

    def test_profile_likes_api_view_is_resolved(self):
        """Test that ProfileLikesAPIView url works correctly."""
        url = reverse('profile_likes', args=['username', ])
        self.assertEquals(
            resolve(url).func.view_class, ProfileLikesAPIView,
        )

    def test_profile_posts_api_view_is_resolved(self):
        """Test that ProfilePostsAPIView url works correctly."""
        url = reverse('profile_posts', args=['username', ])
        self.assertEquals(
            resolve(url).func.view_class, ProfilePostsAPIView,
        )

    def test_long_recommended_posts_api_view_is_resolved(self):
        """Test that LongRecommendedPostsAPIView url works correctly."""
        url = reverse('long_recommended_posts')
        self.assertEquals(
            resolve(url).func.view_class, LongRecommendedPostsAPIView,
        )

    def test_recommended_posts_api_view_is_resolved(self):
        """Test that RecommendedPostsAPIView url works correctly."""
        url = reverse('recommended_posts')
        self.assertEquals(
            resolve(url).func.view_class, RecommendedPostsAPIView,
        )
