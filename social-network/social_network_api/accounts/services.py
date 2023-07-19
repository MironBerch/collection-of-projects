from rest_framework.request import Request

from accounts.models import User, Profile
from accounts.exceptions import (
    AccountDoesNotExistException,
    ProfileDoesNotExistException,
)


def get_user_by_request(request: Request) -> User:
    """
    Function which return user which send a request.
    """

    user = request.user
    return user


def get_user_profile(user: User) -> Profile:
    """
    Function which return user profile.
    """

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise ProfileDoesNotExistException()

    return profile


def get_user_by_username(username: str) -> User:
    """
    Function which return user by username.
    """

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise AccountDoesNotExistException()

    return user


def follow_user(self: User, user: User) -> None:
    """Follow `user`."""
    if user != self:
        self.following.add(user)


def get_followers(user: User):
    """Get users that are following user."""
    return (
        user.followers.filter(is_active=True)
        .select_related('profile')
        .prefetch_related('followers')
        .prefetch_related('following')
    )


def get_following(user: User):
    """Get users that user is following."""
    return (
        user.following.filter(is_active=True)
        .select_related('profile')
        .prefetch_related('followers')
        .prefetch_related('following')
    )


def unfollow(self: User, user: User) -> None:
    """Unfollow `user`."""
    self.following.remove(user)


def get_user_profile_by_request(request: Request) -> Profile:
    return (request.user.profile)


def recommend_users(user: object, long: bool):
    qs = (
        User.objects.all().select_related('profile')
        .exclude(followers=user)
        .exclude(id=user.id)
        .prefetch_related('following')
        .prefetch_related('followers')
        .order_by('?')
    )
    if long is False:
        qs = qs[:7]
    return qs
