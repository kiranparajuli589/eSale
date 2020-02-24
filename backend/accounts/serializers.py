"""
Account App Serializer
"""
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    user_profile = serializers.SerializerMethodField()

    class Meta:
        """
        Meta
        """
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'is_customer', 'is_vendor',
                  'is_superuser', 'is_staff', 'date_of_birth', 'date_joined',
                  'phone', 'user_profile',
                  )

    @staticmethod
    def get_user_profile(user):
        """
        :param user: User
        :return: UserProfile
        """
        # pylint: disable=W0612,E1101
        profile, create = UserProfile.objects.get_or_create(user=user)
        return UserProfileSerializer(profile, read_only=True).data


class UserSerializerCreate(serializers.ModelSerializer):
    """
    User Create Serializer
    """
    class Meta:
        """
        Meta
        """
        fields = ('username', 'password')

    @staticmethod
    def validate_password(password):
        """
        :param password:string
        :return: string
        """
        validate_password(password)
        return password


class UserSerializerLogin(UserSerializer):
    """
    User Login Serializer
    """
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        get or create token
        :param user: User
        :return: string
        """
        # pylint: disable=W0612,E1101
        token, create = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        """
        Meta
        """
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'is_customer', 'is_vendor', 'user_profile',
                  'token',
                  )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer
    """
    class Meta:
        """
        Meta
        """
        model = UserProfile
        fields = '__all__'


class UserProfileSerializerUpdate(serializers.ModelSerializer):
    """
    User Profile Update Serializer
    """
    class Meta:
        """
        Meta
        """
        model = UserProfile
        fields = ('profile_photo', 'photo_doc')
