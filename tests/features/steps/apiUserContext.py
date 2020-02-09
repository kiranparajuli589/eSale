import os

from behave import given, when, then
import requests
from requests import request

from auth_api.views import get_authorization_header

from eSale.settings import CLIENT_ID, CLIENT_SECRET, ESALE_SERVER_BACKEND,\
    GET_TOKEN_URL, LAST_TOKEN, LAST_TOKEN_RESPONSE


@given(u'following users have been created with default attributes')
def step_following_users_have_been_created(context):
    users = {}
    for user in context.table:
        body = {"username": user[0], "email": user[1], "password": user[2]}
        users[user[0]] = body

    for username, body in users.items():
        data = {
            'username': username,
            'email': body["email"],
            'password': body['password'],
        }
        headers = get_authorization_header(request)
        with requests.Session() as s:
            s.headers.update(headers)
            response = s.post(
                url='{}/auth/users/'.format(ESALE_SERVER_BACKEND),
                data=data
            )
        return response.status_code.should.equal(201)


@when('admin sends a get request to retrieve all users')
def step_admin_sends_get_req_to_retrieve_all_users(context):
    pass


@then('users with following attributes should be listed')
def step_users_with_following_attrs_should_be_listed(context):
    headers = get_authorization_header(request)
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(ESALE_SERVER_BACKEND + '/auth/users')
    json_response = response.json()
    for row in context.table:
        pass