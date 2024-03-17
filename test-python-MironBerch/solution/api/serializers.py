from rest_framework import serializers

from api.models import Country, Post


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'alpha2', 'alpha3', 'region')


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Post
        fields = ('content', 'tags')

class ViewPostSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'tags', 'createdAt', 'likesCount', 'dislikesCount')
