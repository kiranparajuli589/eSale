"""
User API View
"""
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
# pylint: disable=E0402
from ..serializers import UserSerializer
from ..models import User


# pylint: disable=R0901
class UsersViewSet(viewsets.ModelViewSet):
    """
    Viewset for User Model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
