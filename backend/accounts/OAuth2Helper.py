import os
import sys
import requests
sys.path.append("/home/kiran/Downloads/ESALE/backend")


class OAuth2Helper:
    def __init__(self):
        self.__CLIENT_ID = os.getenv('CLIENT_ID')
        self.__CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.__ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')
        self.__GET_TOKEN_URL = '{}/auth/token/'.format(self.__ESALE_SERVER_BACKEND)
        self.__LAST_TOKEN = ""
        self.__LAST_TOKEN_RESPONSE = {}

    def __set_token(self, token):
        """
        sets token as present working token
        :param token: (str)
        :return (void)
        """
        self.__LAST_TOKEN = token

    def __set_last_token_response(self, token_response):
        """
        sets lasts token response to global var
        :param token_response: (dict)
        :return (dict)
        """
        self.__LAST_TOKEN_RESPONSE = token_response

    def get_present_token(self, request):
        """
        returns present working token
        :return: (str)
        """
        if not self.__LAST_TOKEN:
            self.admin_get_new_token(request)
        return self.__LAST_TOKEN

    def get_last_token_response(self):
        """
        return last token response
        :return: (dict)
        """
        return self.__LAST_TOKEN_RESPONSE

    def get_authorization_header(self, request):
        """
        :return: (dict)
        """
        token = self.get_present_token(request)
        return {'Authorization': '{} {}'.format('Bearer', token)}

    def admin_get_new_token(self, request):
        """
            Gets tokens with username and password. Input should be in the format:
            :return (void)
        """
        data = {
            'client_id': self.__CLIENT_ID,
            'client_secret': self.__CLIENT_SECRET,
            'grant_type': 'password',
            'username': 'admin',
            'password': 'admin',
        }
        # sending get request and saving the response as response object
        response = requests.post(
            url=self.__GET_TOKEN_URL,
            data=data
        )
        # extracting data in json format
        json_response = response.json()
        self.__set_token(json_response['access_token'])
        self.__set_last_token_response(json_response)

    def refresh_token(self, request):
        """
        Registers user to the server. Input should be in the format:
        {"refresh_token": "<token>"}
        :return (void)
        """
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.__LAST_TOKEN_RESPONSE['refresh_token'],
            'username': 'admin',
            'password': 'password',
            'client_id': self.__CLIENT_ID,
            'client_secret': self.__CLIENT_SECRET
        }
        headers = self.get_authorization_header(request)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.post(
                url=self.__GET_TOKEN_URL,
                data=data
            )
        json_response = response.json()
        self.__set_last_token_response(json_response)
        self.__set_token(json_response)
