import requests
import sure
from requests import request
from django.conf import settings
from behave import given, when, then
from auth_api.views import get_authorization_header


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
                url='{}/auth/users/'.format(settings.ESALE_SERVER_BACKEND),
                data=data
            )
        with sure.ensure('Captured response output: {0}', response.json()):
            response.status_code.should.equal(201)
    return


@when('admin sends a get request to retrieve all users')
def step_admin_sends_get_req_to_retrieve_all_users(context):
    headers = get_authorization_header(request)
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(settings.ESALE_SERVER_BACKEND+'/auth/users')
    json_response = response.json()
    settings.LAST_STD_OUT = json_response
    return


@then('users with following attributes should be listed')
def step_users_with_following_attrs_should_be_listed(context):
    last_std_out = settings.LAST_STD_OUT
    print(last_std_out)
    found = False
    # for row in context.table:
    #     for user in last_std_out:
    #
    #
    # headers = get_authorization_header(request)
    # with requests.Session() as s:
    #     s.headers.update(headers)
    #     response = s.delete(settings.ESALE_SERVER_BACKEND + '/auth/users')