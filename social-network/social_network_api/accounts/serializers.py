from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, Profile


class SignupSerializer(serializers.ModelSerializer):
    """
    Signup API view serializer.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class SigninSerializer(serializers.Serializer):
    """
    Signin API view serializer.

    :param email: Username or email address.
    :param password: Password.
    """

    email = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )


class ProfileSerializer(serializers.ModelSerializer):
    """
    User profile serializer.
    """

    gender = serializers.ChoiceField(
        required=False,
        choices=Profile.GENDER_CHOICES,
    )

    class Meta:
        model = Profile
        fields = (
            'profile_image',
            'profile_banner',
            'gender',
            'description',
        )


class PasswordSerializer(serializers.Serializer):
    """
    Reset password serializer.
    """

    current_password = serializers.CharField(
        min_length=8,
        write_only=True,
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )
    password2 = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    def validate(self, attrs):
        new_password = attrs.get('password')
        confirm_password = attrs.get('password2')
        if new_password != confirm_password:
            raise serializers.ValidationError('New passwords do not match.')
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    followers = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    following = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    profile = ProfileSerializer(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'followers',
            'following',
            'profile',
        )
