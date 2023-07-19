from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from core.mixins import PaginationMixin
from core.permissions import IsOwnerOrReadOnly
from posts.serializers import UserSerializer
from posts.pagination import (
    PostPagination,
    ProfileLikesPagination,
    ReplyPagination,
)
from posts.serializers import (
    PostDetailSerializer,
    PostSerializer,
    ReplySerializer,
    RepostSerializer,
)
from posts.services import (
    get_feed,
    get_active_posts_by_pk,
    get_recommend_posts,
    get_user_post_by_pk,
    get_liked_posts,
    get_user_profile_posts,
    get_post_by_id,
    get_post,
)
from accounts.services import get_user_by_username
from notifications.services import (
    delete_post_notification,
    create_post_notification,
)


class FeedAPIView(ListAPIView):
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_feed(self.request.user)


class LikesAPIView(APIView, PaginationMixin):
    pagination_class = ReplyPagination
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        post = self.get_object(pk)
        request_user = request.user
        post.liked.remove(request_user)
        delete_post_notification(
            from_user=request_user,
            to_user=post.author,
            type=2,
            post=post,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        post = self.get_object(pk)
        users = post.liked.all()
        paginated = self.paginator.paginate_queryset(users, self.request)
        serializer = UserSerializer(paginated, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def get_object(self, pk):
        return get_post(pk)

    def post(self, request, pk):
        post = self.get_object(pk)
        request_user = request.user
        if request_user not in post.liked.all():
            post.liked.add(request_user)
            if request_user != post.author:
                create_post_notification(
                    from_user=request_user,
                    to_user=post.author,
                    type=2,
                    post=post,
                )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)


class LongRecommendedPostsAPIView(ListAPIView):
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_recommend_posts(user=self.request.user, long=True)


class PostAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        parent_post_id = self.request.data.get('parent_id')
        if parent_post_id:
            parent_post = get_post_by_id(id=parent_post_id)
            request_user = self.request.user
            if request_user != parent_post.author:
                create_post_notification(
                    from_user=request_user,
                    to_user=parent_post.author,
                    type=3,
                    post=parent_post,
                )
        serializer.save(author=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = PostDetailSerializer

    def delete(self, request, pk):
        request_user = self.request.user
        post = get_user_post_by_pk(user=request_user, pk=pk)
        post.is_active = False
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return get_active_posts_by_pk(pk=self.kwargs.get('pk'))


class PostRepliesAPIView(ListAPIView):
    pagination_class = ReplyPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = ReplySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        post = get_post(pk=pk)
        return post.get_replies()


class ProfileLikesAPIView(ListAPIView):
    pagination_class = ProfileLikesPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_user_by_username(username=username)
        return get_liked_posts(user=user)


class ProfilePostsAPIView(ListAPIView):
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_user_by_username(username=username)
        return get_user_profile_posts(user=user)


class RepostAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RepostSerializer

    def perform_create(self, serializer):
        parent_post_id = self.request.data.get('parent_id')
        parent_post = get_post_by_id(id=parent_post_id)
        request_user = self.request.user
        if request_user != parent_post.author:
            create_post_notification(
                from_user=request_user,
                to_user=parent_post.author,
                type=1,
                post=parent_post,
            )
        serializer.save(author=request_user)


class RecommendedPostsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_recommend_posts(user=self.request.user)
