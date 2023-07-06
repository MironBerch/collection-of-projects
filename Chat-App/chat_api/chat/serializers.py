from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chat.models import ChatRoom, ChatMessage, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'image',
            'first_name',
            'last_name',
        )


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['userId'] = user.id
        return token


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'email',
            'password',
            'confirm_password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': 'Password fields did not match.'}
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            image=validated_data['image']
        )
        user.set_password(validated_data['password'])
        user.save()
        chatRoom = ChatRoom.objects.create(
            type='SELF', name=user.first_name + user.last_name
        )
        chatRoom.member.add(user.id)
        return user


class ChatRoomSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True, read_only=True)
    members = serializers.ListField(write_only=True)

    def create(self, validatedData):
        memberObject = validatedData.pop('members')
        chatRoom = ChatRoom.objects.create(**validatedData)
        chatRoom.member.set(memberObject)
        return chatRoom

    class Meta:
        model = ChatRoom
        exclude = ['id']


class ChatMessageSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userImage = serializers.ImageField(source='user.image')

    class Meta:
        model = ChatMessage
        exclude = ['id', 'chat']

    def get_userName(self, Obj):
        return Obj.user.first_name + ' ' + Obj.user.last_name
