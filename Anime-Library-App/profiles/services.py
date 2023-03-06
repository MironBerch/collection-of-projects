from django.shortcuts import get_object_or_404

from profiles.models import Profile, ProfileComment


def get_user_profile(user):
    """Get user profile"""
    profile = get_object_or_404(Profile, user=user)
    return profile


def create_profile(user) -> None:
    """Create user profile"""
    Profile.objects.create(user=user)


def get_profile_comments(profile):
    """Get profile comments"""
    comments = ProfileComment.objects.filter(profile=profile)
    return comments


def create_profile_comment(profile, author, content) -> None:
    """Create profile comment at db"""
    ProfileComment.objects.create(
        profile=profile,
        author=author,
        content=content,
    )