from ..models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from ..serializers import (
    UserSerializer,
)


class UsersViewSet(viewsets.ModelViewSet):
    """
    viewset for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [OAuth2Authentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

