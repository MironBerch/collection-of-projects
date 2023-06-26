from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Post
from api.serializers import PostSerializer


class PostView(APIView):
    def get(self, request):
        posts = [
            {
                'content': post.content,
            } for post in Post.objects.all()
        ]
        return Response(posts)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
