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
last_token = ""
last_token_response = {}


def get_present_token():
    global last_token
    if not last_token:
        get_new_token()
    return last_token


def set_token(token):
    global last_token
    last_token = token


def set_last_token_response(token_response):
    global last_token_response
    last_token_response = token_response


def get_last_token_response():
    global last_token_response
    return last_token_response


def get_authorization_header():
    token = get_present_token()
    return {'Authorization': '{} {}'.format('Bearer', token)}


def get_all_users():
    headers = get_authorization_header()

    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(ESALE_SERVER_BACKEND+'/auth/users')

    return response.json()


def get_new_token():
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
    json_response = response.json()
    set_token(json_response['access_token'])
    set_last_token_response(json_response)


def refresh_token():
    """
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    """
    token_response = get_last_token_response()
    data = {
            'grant_type': 'refresh_token',
            'refresh_token': token_response['refresh_token'],
            'username': 'admin',
            'password': 'password',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    headers = get_authorization_header()
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.post(
            url=GET_TOKEN_URL,
            data=data
        )
    json_response = response.json()
    set_last_token_response(json_response)
    set_token(json_response)


def revoke_token(request):
    """
    Method to revoke tokens.
    {"token": "<token>"}
    """
    data = {
            'token': get_present_token(),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
    headers = get_authorization_header()
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.post(
            url='{}/o/revoke_token'.format(ESALE_SERVER_BACKEND),
            data=data
        )
    json_response = response.json()
    set_last_token_response(json_response)
    set_token(json_response['access_token'])
    # If it goes well return sucess message (would be empty otherwise)
    if response.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, response.status_code)
    # Return the error if it goes badly
    return Response(response.json(), response.status_code)
