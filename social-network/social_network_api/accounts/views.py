from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

from core.mixins import PaginationMixin
from accounts.permissions import (
    IsNotAuthenticated,
)
from accounts.serializers import (
    SignupSerializer,
    SigninSerializer,
    ProfileSerializer,
    PasswordSerializer,
    UserSerializer,
)
from accounts.services import (
    get_user_by_request,
    get_user_profile_by_request,
    get_user_by_username,
    get_followers,
    unfollow,
    get_following,
    follow_user,
    recommend_users,
)
from accounts.pagination import UserPagination
from notifications.services import (
    delete_notification,
    create_notification,
)


class SignupAPIView(APIView):
    """
    Signup API view.
    """

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            request.session.set_expiry(0)
            login(request, user)
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SigninAPIView(APIView):
    """
    Signin API view.
    """

    permission_classes = (IsNotAuthenticated,)
    serializer_class = SigninSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            email=email,
            password=password,
        )

        if user is not None:
            login(request, user)
            return Response(
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'message': 'Invalid email or password'}
            )


class SignoutAPIView(APIView):
    """
    Signout API view.
    """

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditPasswordAPIView(UpdateAPIView):
    """
    Edit password API view.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request):
        current_password = request.data.get('current_password')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        if not current_password or not password or not password2:
            return Response(
                {'message': 'Please provide all the required fields.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        if not check_password(current_password, user.password):
            return Response(
                {'message': 'Invalid current password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != password2:
            return Response(
                {'message': 'New passwords do not match.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()

        return Response(
            {'message': 'Password updated successfully.'},
            status=status.HTTP_200_OK,
        )


class EditProfileAPIView(UpdateAPIView):
    """
    Edit profile API view.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_user_profile_by_request(request=self.request)


class EditUserAPIView(UpdateAPIView):
    """
    Edit user API view.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return get_user_by_request(request=self.request)


class FollowersAPIView(ListAPIView):
    """
    Get list of `user`'s followers.
    """

    pagination_class = UserPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = get_user_by_username(username=self.kwargs.get('username'))
        return get_followers(user=user)


class FollowingAPIView(APIView, PaginationMixin):
    pagination_class = UserPagination
    permission_classes = (IsAuthenticated,)

    def _get_object(self, username):
        return get_user_by_username(username=username)

    def delete(self, request, username):
        user = self._get_object(username)
        request_user = get_user_by_request(request=request)
        unfollow(self=request_user, user=user)
        if request_user != user:
            delete_notification(
                from_user=request_user,
                to_user=user,
                type=4,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, username):
        user = self._get_object(username)
        following = get_following(user=user)
        paginated = self.paginator.paginate_queryset(following, self.request)
        serializer = UserSerializer(paginated, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, username):
        user = self._get_object(username)
        request_user = get_user_by_request(request=request)
        follow_user(self=request_user, user=user)
        if request_user != user:
            create_notification(
                from_user=request_user,
                to_user=user,
                type=4,
            )
        return Response(status=status.HTTP_201_CREATED)


class LongRecommendedUsersAPIView(ListAPIView):
    pagination_class = UserPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = get_user_by_request(request=self.request)
        return recommend_users(user=user, long=True)


class RecommendedUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = get_user_by_request(request=self.request)
        return recommend_users(user=user, long=False)


class UserDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return get_user_by_username(username=self.kwargs.get('username'))
