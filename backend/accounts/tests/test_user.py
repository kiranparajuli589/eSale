"""
Users API Test
"""
import os
import requests
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import authenticate
from ..token_helper import TokenHelper


def authenticate_user(username, password):
    """
    Args:
        username(str): username
        password(str): password
    Returns:
       JsonResponse
    """
    test_user = authenticate(username=username, password=password)
    print(type(test_user))


class UserTest(APITestCase):
    """
    User API Test Class
    """

    def setUp(self):
        """
        :return: void
        """
        self.client = APIClient()
        self.token_helper = TokenHelper()
        self.__esale_server_backend = 'http://' + os.getenv('ESALE_SERVER_BACKEND')

    def test_get_all_users(self):
        """
        returns json response of all created users
        Returns:
             dict: json response of get request
        """
        headers = TokenHelper.get_authorization_header(self.token_helper)
        print(self.__esale_server_backend)
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(self.__esale_server_backend + '/api/v1/users/')
        print(response)
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
        headers = TokenHelper.get_authorization_header(self.token_helper)
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get('{}/api/v1/users/1/'.format(self.__esale_server_backend))
        self.assertEqual(
            response.status_code,
            200
        )
