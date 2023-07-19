from django.urls import path

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


urlpatterns = [
    path(
        route='',
        view=PostAPIView.as_view(),
        name='post',
    ),
    path(
        route='repost/',
        view=RepostAPIView.as_view(),
        name='repost',
    ),
    path(
        route='<int:pk>/',
        view=PostDetailAPIView.as_view(),
        name='post_detail',
    ),
    path(
        route='<int:pk>/likes/',
        view=LikesAPIView.as_view(),
        name='likes',
    ),
    path(
        route='<int:pk>/replies/',
        view=PostRepliesAPIView.as_view(),
        name='replies',
    ),
    path(
        route='feed/',
        view=FeedAPIView.as_view(),
        name='feed',
    ),
    path(
        route='profile/<str:username>/likes/',
        view=ProfileLikesAPIView.as_view(),
        name='profile_likes',
    ),
    path(
        route='profile/<str:username>/posts/',
        view=ProfilePostsAPIView.as_view(),
        name='profile_posts',
    ),
    path(
        route='long-recommended-posts/',
        view=LongRecommendedPostsAPIView.as_view(),
        name='long_recommended_posts',
    ),
    path(
        route='recommended-posts/',
        view=RecommendedPostsAPIView.as_view(),
        name='recommended_posts',
    ),
]
