import os
import requests
from django.contrib.auth import authenticate
from OAuth2Helper import OAuth2Helper
from django.conf import settings
settings.configure()
from rest_framework.test import APIClient, APITestCase


def authenticate_user(username, password):
    """
    Args:
        username(str): username
        password(str): password
    Returns:
       JsonResponse
    """
    test_user = authenticate(username=username, password=password)
    print(test_user)
    print(type(test_user))


class UserTest(APITestCase):
    def __init__(self):
        super().__init__()
        self.client = APIClient()
        self.OAuth2Helper = OAuth2Helper()
        self.__ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')

    def get_all_users(self, request):
        """
        returns json response of all created users
        Args:
             request (object)
        Returns:
             dict: json response of get request
        """
        headers = OAuth2Helper.get_authorization_header(self.OAuth2Helper, request)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.get(self.__ESALE_SERVER_BACKEND + '/api/v1/users/')
        self.assertEqual(
            response.status_code,
            200
        )

    def get_a_user(self, request, user_id):
        """
        returns user with given user_id
        Args:
            request (object)
            user_id: (str) user id of expected user
        Returns:
            dict: JsonResponse of get request
        """
        headers = OAuth2Helper.get_authorization_header(self.OAuth2Helper, request)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.get('{}/api/v1/users/{}/'.format(self.__ESALE_SERVER_BACKEND, user_id))
        self.assertEqual(
            response.status_code,
            200
        )
