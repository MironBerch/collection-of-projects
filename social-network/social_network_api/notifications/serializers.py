from rest_framework import serializers

from posts.serializers import PostSerializer
from accounts.serializers import UserSerializer
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    post = PostSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Notification
        fields = (
            'created_at',
            'from_user',
            'id',
            'post',
            'to_user',
            'type',
        )
