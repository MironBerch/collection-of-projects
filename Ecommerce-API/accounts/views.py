from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from accounts.models import (
    Address,
    PhoneNumber,
    Profile,
)
from accounts.permissions import (
    IsUserAddressOwner,
    IsUserProfileOwner,
)
from accounts.serializers import (
    AddressReadOnlySerializer,
    PhoneNumberSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    VerifyPhoneNumberSerialzier,
)


class UserRegisterationAPIView(RegisterView):
    """
    Register new users using phone number or email address and password.
    """
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = ''

        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)

        if email and phone_number:
            res = SendOrResendSMSAPIView.as_view()(request._request, *args, **kwargs)

            if res.status_code == 200:
                response_data = {
                    'detail': _('Verification email and SMS sent.')
                }

        elif email and not phone_number:
            response_data = {
                'detail': _('Verification email sent.')
            }

        else:
            res = SendOrResendSMSAPIView.as_view()(request._request, *args, **kwargs)

            if res.status_code == 200:
                response_data = {
                    'detail': _('Verification SMS sent.')
                }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using phone number or email address and password.
    """
    serializer_class = UserLoginSerializer


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        if serializer.is_valid():
            # Send OTP
            phone_number = str(
                serializer.validated_data['phone_number'],
            )

            user = User.objects.filter(
                phone__phone_number=phone_number,
            ).first()

            sms_verification = PhoneNumber.objects.filter(
                user=user,
                is_verified=False,
            ).first()

            sms_verification.send_confirmation()

            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches and verify the user.
    """
    serializer_class = VerifyPhoneNumberSerialzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        if serializer.is_valid():
            message = {
                'detail': _('Phone number successfully verified.'),
            }
            return Response(
                message,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class GoogleLogin(SocialLoginView):
    """
    Social authentication with Google.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'call_back_url'
    client_class = OAuth2Client


class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user `Profile`.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsUserProfileOwner, )

    def get_object(self):
        return self.request.user.profile


class UserAPIView(RetrieveAPIView):
    """
    Get `User` details.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses.
    """
    queryset = Address.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner, )

    def get_queryset(self):
        return (
            super().get_queryset().filter(
                user=self.request.user,
            )
        )
