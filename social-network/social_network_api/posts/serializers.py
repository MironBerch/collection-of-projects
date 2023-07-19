from rest_framework import serializers

from accounts.serializers import UserSerializer
from posts.models import Post


class PostParentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'content',
            'created_at',
        )


class BasePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    content = serializers.CharField(allow_blank=True)
    is_author = serializers.SerializerMethodField()
    parent = PostParentSerializer(read_only=True)
    parent_id = serializers.IntegerField(
        required=False,
        write_only=True,
        allow_null=True,
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'content',
            'created_at',
            'id',
            'is_active',
            'is_author',
            'is_reply',
            'liked',
            'parent',
            'parent_id',
        ]

    def get_is_author(self, obj):
        request = self.context.get('request')
        return obj.author == request.user


class PostSerializer(BasePostSerializer):
    reply_ids = serializers.ListField(read_only=True)
    repost_ids = serializers.ListField(read_only=True)

    class Meta:
        model = Post
        fields = BasePostSerializer.Meta.fields + [
            'reply_ids',
            'repost_ids',
        ]


class RepostSerializer(BasePostSerializer):
    content = serializers.CharField(allow_blank=True)


class ReplySerializer(BasePostSerializer):
    pass


class PostDetailSerializer(PostSerializer):
    extra_kwargs = {
        'created_at': {'read_only': True},
        'id': {'read_only': True},
        'is_reply': {'read_only': True},
        'parent_id': {'read_only': True},
    }
