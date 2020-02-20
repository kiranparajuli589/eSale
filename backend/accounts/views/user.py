from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from ..models import UserProfile, User, UserActivationCode
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from ..serializers import (
    UserSerializer,
    UserSerializerCreate,
    UserSerializerLogin,
    UserSerializerUpdate
)


class UsersViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [OAuth2Authentication]

    @action(detail=False, methods=["post"])
    def post(self, request):
        """
        Create user
        """
        serializer = UserSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.is_active = True
            user.save()
            user = get_object_or_404(User, email=request.data.get('username'))
            code_object = UserActivationCode.objects.create(user=user)
            code = code_object.code
            current_site = get_current_site(request)
            mail_subject = 'Welcome To ESALE.'
            message = render_to_string('user_activation.html', {
                'user': user.username,
                'domain': current_site.domain,
                'code': code,
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            UserProfile(user=user).save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get(self, request, pk=None):
        """
        View individual user
        """

        user = get_object_or_404(User, pk=pk)
        return Response(UserSerializer(user).data)

    @action(detail=True, methods=['patch'])
    def patch(self, request, pk=None):
        """
        Update authenticated user
        """

        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializerUpdate(user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializerLogin(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        """
        Delete user
        """

        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def verify_token(request):
    try:
        current_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        if current_token in str(Token.objects.all()):
            return Response('Yes')
        else:
            return Response('Token does not exist.', status=status.HTTP_404_NOT_FOUND)
    except NotFound:
        return Response("No Token.", status=status.HTTP_404_NOT_FOUND)
