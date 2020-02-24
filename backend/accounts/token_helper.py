"""
Token Helper
"""
import os
import re
import requests


class TokenHelper:
    """
    Token Helper Class
    """
    def __init__(self):
        self.__esale_server_backend = 'http://' + os.getenv('ESALE_SERVER_BACKEND')
        self.__last_token = ""
        self.__admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        self.__admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    def __set_token(self, token):
        """
        sets token as present working token
        :param token: (str)
        :return (void)
        """
        self.__last_token = token

    def get_present_token(self):
        """
        returns present working token
        :return: (str)
        """
        if not self.__last_token:
            self.admin_get_new_token()
        return self.__last_token

    def get_authorization_header(self):
        """
        :return: (dict)
        """
        token = self.get_present_token()
        return {'Authorization': '{} {}'.format('Token', token)}

    def admin_get_new_token(self):
        """
            Gets tokens with username and password. Input should be in the format:
            :return (void)
        """
        data = {
            'username': self.__admin_username,
            'password': self.__admin_password
        }
        response = requests.post(
            url='{}/token/'.format(self.__esale_server_backend),
            data=data
        )
        token_response = response.content.decode("ASCII")
        token_regex = re.compile(r'^{"token":"(.*)"}$')
        result = token_regex.search(token_response)
        token = result.group(1)
        self.__set_token(token)
