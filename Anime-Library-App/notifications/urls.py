from django.urls import path

from notifications.views import NotificationView, read_notifications, delete_notifications


urlpatterns = [
    path(
        route='<str:username>/messages/notifications/',
        view=NotificationView.as_view(),
        name='notification_view',
    ),
    path(
        route='messages/notifications/read/',
        view=read_notifications,
        name='read_notifications',
    ),
    path(
        route='messages/notifications/delete/',
        view=delete_notifications,
        name='delete_notifications',
    ),
]