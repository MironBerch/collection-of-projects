from django.shortcuts import get_object_or_404

from notifications.models import Notification
from accounts.models import User
from posts.models import Post


def get_notification(pk, to_user):
    return get_object_or_404(
        Notification,
        pk=pk,
        to_user=to_user,
    )


def get_user_notification(to_user: User):
    return Notification.objects.filter(
        to_user=to_user,
    )


def count_user_notification(
        request_user: User
):
    return Notification.objects.filter(
        to_user=request_user,
        created_at__gt=request_user.last_notification_read_time,
    ).count()


def create_notification(
        from_user: User,
        to_user: User,
        type: int,
):
    return Notification.objects.create(
        from_user=from_user,
        to_user=to_user,
        type=type,
    )


def delete_notification(
        from_user: User,
        to_user: User,
        type: int,
):
    return Notification.objects.filter(
        from_user=from_user,
        to_user=to_user,
        type=type,
    ).delete()


def create_post_notification(
        from_user: User,
        to_user: User,
        type: int,
        post: Post
):
    return Notification.objects.create(
        from_user=from_user,
        to_user=to_user,
        type=type,
        post=post,
    )


def delete_post_notification(
        from_user: User,
        to_user: User,
        type: int,
        post: Post
):
    return Notification.objects.filter(
        from_user=from_user,
        to_user=to_user,
        type=type,
        post=post,
    ).delete()
