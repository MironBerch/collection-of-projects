from django.shortcuts import get_object_or_404

from accounts.models import User
from posts.models import Post


def get_feed(user: User):
    return Post.objects.feed(user)


def get_active_posts_by_pk(pk: int):
    return (
        Post.objects.filter(
            pk=pk,
        ).active()
    )


def get_recommend_posts(user: User, long: bool = False):
    return Post.objects.recommend_posts(user=user, long=long)


def get_user_post_by_pk(user: User, pk: int):
    return get_object_or_404(
        Post,
        author=user,
        pk=pk,
        is_active=True,
    )


def get_liked_posts(user: User):
    return Post.objects.posts().filter(liked=user)


def get_user_profile_posts(user: User):
    return Post.objects.profile_posts(user)


def get_post_by_id(id: int):
    return get_object_or_404(Post, id=id)


def get_post(pk: int):
    return get_object_or_404(
        Post,
        pk=pk,
        is_active=True,
    )
