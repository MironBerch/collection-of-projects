from notifications.models import Notification


def get_user_notifications(user):
    notifications = Notification.objects.filter(user=user)
    return notifications


def read_user_notifications(notifications):
    for notification in notifications:
        notification.is_seen = True
        notification.save()


def delete_user_notifications(notifications):
    for notification in notifications:
        notification.delete()