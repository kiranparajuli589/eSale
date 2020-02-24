"""
Account Models: UserManager, User, UserProfile, UserActivationCode, PasswordResetCode
"""
import os
import random
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


def upload_posts_media_to(instance, filename):
    """
    :param instance: user instance
    :param filename: media
    :return: string
    """
    username = instance.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'photos/{username}/{filename}'


class UserManager(BaseUserManager):
    """
    User Model Customization
    """
    use_in_migrations = True

    def _create_user(self, username, password, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        :param username: string
        :param password: string
        :param extra_fields: extra user args
        :return: void
        """
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(username, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model
    """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, default=None)
    first_name = models.CharField(max_length=255, default=None, null=True)
    last_name = models.CharField(max_length=255, default=None, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    phone = models.CharField(max_length=10, unique=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, default=None)

    GENDER_CHOICES = (
        (None, None),
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
        default=None,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_short_name(self):
        """
        :return: string
        """
        return self.first_name

    def get_full_name(self):
        """
        :return: string
        """
        return self.first_name + self.last_name

    def get_email_address(self):
        """
        :return: string
        """
        return self.email

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if not self.password:
            self.password = str(uuid.uuid4()).replace('-', '')
        super(User, self).save(*args, **kwargs)


class UserProfile(models.Model):
    """
    User Profile Model
    """
    profile_photo = models.ImageField(
        null=True, upload_to=upload_posts_media_to, default=None)
    is_verified = models.BooleanField(default=False)
    pending_verification = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # pylint: disable=E1101
        return self.user.username


class ResetPasswordCode(models.Model):
    """
    ResetPasswordCode Model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        """
        Meta
        """
        default_related_name = 'reset_password_codes'

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.user.username} - {self.code}'


class UserActivationCode(models.Model):
    """
    UserActivationCode Model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        """
        Meta
        """
        default_related_name = 'activation_codes'

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.user.username} - {self.code}'
