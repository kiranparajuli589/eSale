import os
import re
import requests


class TokenHelper:
    def __init__(self):
        self.__ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')
        self.__LAST_TOKEN = ""
        self.__ADMIN_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
        self.__ADMIN_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    def __set_token(self, token):
        """
        sets token as present working token
        :param token: (str)
        :return (void)
        """
        self.__LAST_TOKEN = token

    def get_present_token(self):
        """
        returns present working token
        :return: (str)
        """
        if not self.__LAST_TOKEN:
            self.admin_get_new_token()
        return self.__LAST_TOKEN

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
            'username': self.__ADMIN_USERNAME,
            'password': self.__ADMIN_PASSWORD
        }
        response = requests.post(
            url='{}/token/'.format(self.__ESALE_SERVER_BACKEND),
            data=data
        )
        token_response = response.content.decode("ASCII")
        token_regex = re.compile(r'^{"token":"(.*)"}$')
        result = token_regex.search(token_response)
        token = result.group(1)
        self.__set_token(token)
