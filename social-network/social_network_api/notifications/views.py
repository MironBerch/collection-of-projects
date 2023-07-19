from rest_framework import status
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from notifications.pagination import NotificationPagination
from notifications.serializers import NotificationSerializer
from notifications.services import (
    get_notification,
    get_user_notification,
    count_user_notification,
)


class UnreadNotificationCountAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request_user = request.user
        count = count_user_notification(request_user=request_user)
        return Response(count, status=status.HTTP_200_OK)


class NotificationsAPIView(ListAPIView):

    pagination_class = NotificationPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        request_user = self.request.user
        request_user.last_notification_read_time = now()
        request_user.save()
        return get_user_notification(
            to_user=self.request.user,
        )


class RemoveNotificationAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        notification = get_notification(pk=pk, to_user=request.user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
