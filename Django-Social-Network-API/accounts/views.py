from django.contrib.auth import login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from accounts.serializers import UserSerializer, RegisterSerializer


class SignupView(generics.GenericAPIView):
    """
    Sign up genericAPIView which use knox.
    """
    
    queryset = None
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'user': UserSerializer(
                    user,
                    context=self.get_serializer_context(),
                ).data,
                'token': AuthToken.objects.create(user)[1],
            }
        )


class SigninView(KnoxLoginView):
    """
    Sign in KnoxLoginView.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        user = serializer.validated_data['user']
        login(request, user)
        return super(
            SigninView, self,
        ).post(request, format=None)
