import os
import requests
from django.http import JsonResponse
from rest_framework.response import Response

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ESALE_SERVER_BACKEND = 'http://' + os.getenv('ESALE_SERVER_BACKEND')
GET_TOKEN_URL = '{}/o/token/'.format(ESALE_SERVER_BACKEND)
last_token = ""
last_token_response = {}


def get_present_token():
    """
    returns present working token
    :return: (str)
    """
    global last_token
    if not last_token:
        admin_get_new_token()
    return last_token


def set_token(token):
    """
    sets token as present working token
    :param token: (str)
    :return (void)
    """
    global last_token
    last_token = token


def set_last_token_response(token_response):
    """
    sets lasts token response to global var
    :param token_response: (dict)
    :return (dict)
    """
    global last_token_response
    last_token_response = token_response


def get_last_token_response():
    """
    return last token response
    :return: (dict)
    """
    global last_token_response
    return last_token_response


def get_authorization_header():
    """
    :return: (dict)
    """
    token = get_present_token()
    return {'Authorization': '{} {}'.format('Bearer', token)}


def admin_get_new_token():
    """
        Gets tokens with username and password. Input should be in the format:
        :return (void)
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
    :return (void)
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
    Method to revoke/officially un-register tokens.
    {"token": "<token>"}
    :return (void)
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


def get_all_users(request):
    """
    returns json response of all created users
    Args:
         request (object)
    Returns:
         dict: json response of get request
    """
    headers = get_authorization_header()
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(ESALE_SERVER_BACKEND+'/auth/users')
    json_response = response.json()
    return JsonResponse(json_response, safe=False)


def get_a_user(request, user_id):
    """
    returns user with given user_id
    Args:
        request (object)
        user_id: (str) user id of expected user
    Returns:
        dict: JsonResponse of get request
    """
    headers = get_authorization_header()
    print('here')
    print(headers)
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(ESALE_SERVER_BACKEND + '/auth/users/' + user_id + '/`+1*9')
    json_response = response.json()
    return JsonResponse(json_response, safe=False)
