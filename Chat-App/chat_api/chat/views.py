from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from chat.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
    ChatRoomSerializer,
    ChatMessageSerializer,
)
from chat.models import ChatRoom, ChatMessage, User


class ChatRoomView(APIView):
    def get(self, request, userId):
        chatRooms = ChatRoom.objects.filter(member=userId)
        serializer = ChatRoomSerializer(
            chatRooms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        roomId = self.kwargs['roomId']
        return (
            ChatMessage.objects.filter(
                chat__roomId=roomId
            ).order_by('-timestamp')
        )


class UserView(ListAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        excludeUsersArr = []
        try:
            excludeUsers = self.request.query_params.get('exclude')
            if excludeUsers:
                userIds = excludeUsers.split(',')
                for userId in userIds:
                    excludeUsersArr.append(int(userId))
        except:
            return []
        return super().get_queryset().exclude(id__in=excludeUsersArr)


class LoginApiView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class SignupApiView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer
