from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate

from api.models import Country, Post, Tag
from api.paginators import CustomPagination
from api.serializers import CountrySerializer, PostSerializer, ViewPostSerializer
from users.authentication import JWTAuthentication
from users.models import Friend, User
from users.serializers import (
    FriendSerializer,
    RegisterUserSerializer,
    SigninSerializer,
    UserSerializer,
)
from users.services import create_token, user_tokens_to_black, validate_custom_password


class PingView(APIView):
    def get(self, request):
        return Response('ok', status=status.HTTP_200_OK)


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all()
        region = self.request.query_params.get('region', None)

        if region:
            queryset = queryset.filter(region=region)

        queryset = queryset.distinct('name')

        return queryset


class CountryRetrieveAPIView(APIView):
    def get(self, request, alpha2, format=None):
        country = Country.objects.filter(alpha2=alpha2).first()

        if not country:
            return Response(
                {'reason': 'No country with alpha2.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CountrySerializer(country)
        return Response(serializer.data)


class RegisterAPIView(APIView):
    """
    Signup API view.
    """

    serializer_class = RegisterUserSerializer

    def post(self, request):
        login = request.data.get('login')
        email = request.data.get('email')
        phone = request.data.get('phone')
        if User.objects.filter(login=login).exists():
            return Response(
                {'reason': 'User with this login exists.'},
                status=status.HTTP_409_CONFLICT,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {'reason': 'User with this email exists.'},
                status=status.HTTP_409_CONFLICT,
            )
        if phone and phone != '' and User.objects.filter(phone=phone).exists():
            return Response(
                {'reason': 'User with this phone exists.'},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'profile': UserSerializer(user).data,
            }
            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            #  serializer.errors,
            {'reason': 'Invalid country code or you does not write a required field.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SigninAPIView(APIView):
    serializer_class = SigninSerializer

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            login=login,
            password=password,
        )

        if user is not None:
            return Response(
                {'token': create_token(user.pk)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'reason': 'Invalid login or password.'},
            )


class ProfileEditAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        user = request.user
        login = request.data.get('login')
        email = request.data.get('email')
        phone = request.data.get('phone')
        if user.login != login:
            if User.objects.filter(login=login).exists():
                return Response(
                    {'reason': 'User with this login exists.'},
                    status=status.HTTP_409_CONFLICT,
                )
        if user.email != email:
            if User.objects.filter(email=email).exists():
                return Response(
                    {'reason': 'User with this email exists.'},
                    status=status.HTTP_409_CONFLICT,
                )
        if user.phone != phone:
            if phone and phone != '' and User.objects.filter(phone=phone).exists():
                return Response(
                    {'reason': 'User with this phone exists.'},
                    status=status.HTTP_409_CONFLICT,
                )
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response({'reason': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request, login):
        try:
            user = User.objects.get(login=login)
            if user.login == request.user.login:
                serializer = UserSerializer(user)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            try:
                is_curent_user_friend = Friend.objects.get(user=user, friend=request.user)
            except:
                return Response(
                    {'reason': 'User does not exist or exist but you are not friend.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if user.is_public == True or is_curent_user_friend:
                serializer = UserSerializer(user)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                {'reason': 'User does not exist or exist but you are not friend.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception:
            return Response(
                {'reason': 'User does not exist or exist but you are not friend.'},
                status=status.HTTP_403_FORBIDDEN,
            )


class UpdatePasswordAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        if not user.check_password(request.data.get('oldPassword')):
            return Response(
                {'reason': 'It is not your current password.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        new_password = request.data.get('newPassword')
        if not validate_custom_password:
            return Response(
                {'reason': 'No secure password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        user_tokens_to_black(user.pk)
        return Response(
            {'status': 'ok'},
            status=status.HTTP_200_OK,
        )


class AddFriendsAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        friend_login = request.data.get('login')
        if friend_login == user.login:
            return Response(
                {'status': 'ok'},
                status=status.HTTP_200_OK,
            )
        try:
            friend = User.objects.get(login=friend_login)
            Friend.objects.get_or_create(user=user, friend=friend)
            return Response(
                {'status': 'ok'},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {'status': 'User with this login does not exist.'},
                status=status.HTTP_404_NOT_FOUND,
            )


class RemoveFriendsAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        friend_login = request.data.get('login')
        if friend_login == user.login:
            return Response(
                {'status': 'ok'},
                status=status.HTTP_200_OK,
            )
        try:
            friend = User.objects.get(login=friend_login)
            try:
                friend_object = Friend.objects.get(user=user, friend=friend)
                friend_object.delete()
            except Exception:
                pass
            return Response(
                {'status': 'ok'},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {'status': 'ok'},
                status=status.HTTP_200_OK,
            )


class FriendsAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        friends = Friend.objects.filter(user=user).order_by('-addedAt')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(friends, request)
        serializer = FriendSerializer(result_page, many=True)

        return Response(serializer.data)


class CreatePostAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']
            tag_names = serializer.validated_data['tags']
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            post = Post.objects.create(content=content)
            post.tags.add(*tags)
            view_serializer = ViewPostSerializer(post)
            return Response(view_serializer.data, status=status.HTTP_200_OK)
        return Response({'reason': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class DetailPostAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
            serializer = ViewPostSerializer(data=request.data)
            is_curent_user_friend = None
            try:
                is_curent_user_friend = Friend.objects.get(user=post.author, friend=request.user)
            except:
                is_curent_user_friend = None
            if post.author.is_public or is_curent_user_friend:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'reason': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'reason': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
