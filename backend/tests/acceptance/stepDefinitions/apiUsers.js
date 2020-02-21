const {Given, When, Then} = require('cucumber');
const {client} = require('nightwatch-api');
const httpHelper = require('./../helpers/httpRequest')


Given('user {string} has been deleted', function (string) {
    // Write code here that turns the phrase above into concrete actions
    console.log('pending');
});


When('the administrator sends a user creation request for user {string} password {string} using POST request',
    async function (username, password) {
        const apiURL = client.globals.backend_url + '/users/'
        const status = await httpHelper.httpGetRequest(apiURL, 1)
        console.log(status)
        const body = {
            'username': 'testnightwatch',
            'password': '12345'
        }

        const status1 = await httpHelper.httpPostRequest(apiURL, body)
        console.log(status1)
    });


When('the HTTP status code should be {string}', function (statusCode) {
    // Write code here that turns the phrase above into concrete actions
    console.log('pending');
});

When('user {string} should exist', function (username) {
    // Write code here that turns the phrase above into concrete actions
    console.log('pending');
});



