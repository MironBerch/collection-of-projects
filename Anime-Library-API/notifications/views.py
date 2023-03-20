from django.views import View
from django.shortcuts import redirect
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from notifications.services import get_user_notifications, read_user_notifications, delete_user_notifications


class NotificationView(
    LoginRequiredMixin,
    TemplateResponseMixin,
    View,
    ):
    
    template_name = 'notifications/notifications_view.html'

    def get(self, request, username):
        notifications = get_user_notifications(user=request.user)
        return self.render_to_response(
            context={
                'notifications': notifications,
            },
        )
    

def read_notifications(request):
    notifications = get_user_notifications(user=request.user)
    read_user_notifications(notifications=notifications)
    return redirect('notification_view', username=request.user.username)


def delete_notifications(request):
    notifications = get_user_notifications(user=request.user)
    delete_user_notifications(notifications=notifications)
    return redirect('notification_view', username=request.user.username)