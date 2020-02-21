from .models import UserProfile, User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'is_customer', 'is_vendor',
                  'is_superuser', 'is_staff', 'date_of_birth', 'date_joined',
                  'phone', 'user_profile',
                  )

    @staticmethod
    def get_user_profile(user):
        """
        Get or create profile
        """

        profile, created = UserProfile.objects.get_or_create(user=user)
        return UserProfileSerializer(profile, read_only=True).data


class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'password')

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """
        validate_password(password)
        return password


class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'is_customer', 'is_vendor', 'user_profile',
                  'token',
                  )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('profile_photo', 'photo_doc')
