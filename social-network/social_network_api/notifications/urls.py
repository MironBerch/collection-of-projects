from django.urls import path

from notifications.views import (
    UnreadNotificationCountAPIView,
    NotificationsAPIView,
    RemoveNotificationAPIView,
)


urlpatterns = [
    path(
        route='',
        view=NotificationsAPIView.as_view(),
        name='notifications',
    ),
    path(
        route='<int:pk>/',
        view=RemoveNotificationAPIView.as_view(),
        name='remove_notification',
    ),
    path(
        route='unread-count/',
        view=UnreadNotificationCountAPIView.as_view(),
        name='unread_count',
    ),
]
