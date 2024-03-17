from rest_framework import serializers

from api.models import Country
from users.models import Friend, User


class RegisterUserSerializer(serializers.ModelSerializer):
    countryCode = serializers.CharField(max_length=2)
    isPublic = serializers.BooleanField()

    def validate_countryCode(self, value):
        try:
            Country.objects.get(alpha2=value.upper())
        except Country.DoesNotExist:
            raise serializers.ValidationError('Invalid country code')
        return value.upper()

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
        image = validated_data.pop('image', '')
        user = User.objects.create_user(
            email=validated_data['email'],
            login=validated_data['login'],
            phone=phone,
            image=image,
            country_code=validated_data['countryCode'].upper(),
            is_public=validated_data['isPublic'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = (
            'login',
            'email',
            'phone',
            'countryCode',
            'isPublic',
            'image',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    countryCode = serializers.CharField(source='country_code')
    isPublic = serializers.BooleanField(source='is_public')
    image = serializers.CharField()

    def validate_countryCode(self, value):
        try:
            Country.objects.get(alpha2=value)
        except Country.DoesNotExist:
            raise serializers.ValidationError('Invalid country code')
        return value

    def validate_image(self, value):
        if len(value) > 200:
            raise serializers.ValidationError('Image length cannot be more 200 characters')
        return value

    class Meta:
        model = User
        fields = (
            'login',
            'email',
            'countryCode',
            'isPublic',
            'phone',
            'image',
        )

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        if data.get('image') == '':
            data.pop('image')
        return data


class SigninSerializer(serializers.Serializer):
    login = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(
        min_length=6,
        max_length=100,
        write_only=True,
    )


class FriendSerializer(serializers.ModelSerializer):
    login = serializers.SerializerMethodField()
    addedAt = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)

    def get_login(self, obj):
        return obj.friend.login

    class Meta:
        model = Friend
        fields = ('login', 'addedAt')
