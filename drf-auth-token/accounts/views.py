from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.serializers import SignupSerializer


class SignupAPIView(APIView):
    """
    Signup view.
    """

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(
                    user=user,
                )
                json = serializer.data
                json['token'] = token.key
                return Response(
                    json,
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SigninAPIView(APIView):
    """
    Signin view.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            email=email,
            password=password,
        )

        if user is not None:
            token = Token.objects.get(
                user=user,
            )
            return Response(
                token.key,
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data={'message': 'Invalid email or password'}
            )
