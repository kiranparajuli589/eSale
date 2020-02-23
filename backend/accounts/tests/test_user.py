import os
import requests
from ..TokenHelper import TokenHelper
from django.contrib.auth import authenticate
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
    def setUp(self):
        self.client = APIClient()
        self.OAuth2Helper = TokenHelper()
        self.__ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')

    def test_get_all_users(self):
        """
        returns json response of all created users
        Returns:
             dict: json response of get request
        """
        headers = TokenHelper.get_authorization_header(self.OAuth2Helper)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.get(self.__ESALE_SERVER_BACKEND + '/api/v1/users/')
        self.assertEqual(
            response.status_code,
            200
        )

    def test_get_a_user(self):
        """
        returns user with given user_id
        Returns:
            dict: JsonResponse of get request
        """
        headers = TokenHelper.get_authorization_header(self.OAuth2Helper)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.get('{}/api/v1/users/1/'.format(self.__ESALE_SERVER_BACKEND))
        self.assertEqual(
            response.status_code,
            200
        )
