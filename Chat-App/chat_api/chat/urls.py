from django.urls import path
from chat.views import (
    UserView,
    LoginApiView,
    SignupApiView,
    ChatRoomView,
    MessagesView,
)


urlpatterns = [
    path('users', UserView.as_view()),
    path('login', LoginApiView.as_view()),
    path('signup', SignupApiView.as_view()),
    path('chats', ChatRoomView.as_view()),
    path('chats/<str:roomId>/messages', MessagesView.as_view()),
    path('users/<int:userId>/chats', ChatRoomView.as_view()),
]
