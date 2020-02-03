import os
import requests
from django.http import HttpResponse, HttpRequest
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')
GET_TOKEN_URL = '{}/o/token/'.format(ESALE_SERVER_BACKEND)


def get_my_user(request):
    token_response = get_token(request)
    print(token_response)
    token = token_response['access_token']
    token_type = token_response['token_type']
    headers = {'Authorization': '{} {}'.format(token_type, token)}

    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(ESALE_SERVER_BACKEND+'/auth/users')

    return response.json()


# @api_view(['POST'])
# @permission_classes([AllowAny])
def get_token(request):
    """
        Gets tokens with username and password. Input should be in the format:
        {"username": "username", "password": "password"}
    """
    data = {
        'grant_type': 'password',
        'username': 'admin',
        'password': 'admin',
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    # sending get request and saving the response as response object
    response = requests.post(
        url=GET_TOKEN_URL,
        auth=auth,
        data=data
    )
    # extracting data in json format
    return response.json()


def refresh_token(request):
    """
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    """
    data = {
            'grant_type': 'refresh_token',
            'username': 'admin',
            'password': 'password',
        }
    # auth = (CLIENT_ID, CLIENT_SECRET)

    r = requests.post(
        GET_TOKEN_URL,
        auth=auth,
        data=data
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        '{}/o/revoke_token/'.format(ESALE_SERVER_BACKEND),
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
