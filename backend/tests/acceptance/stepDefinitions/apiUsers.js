const {Given, When, Then} = require('cucumber');
const {client} = require('nightwatch-api');
const httpHelper = require('./../helpers/httpRequest')
const assert = require('assert')


Given('user {string} has been deleted', function (string) {
    // Write code here that turns the phrase above into concrete actions
    console.log('pending');
});

When('the administrator sends a detail of user with id {string} using restAPI GET request',
    async function (userId) {
        const apiURL = client.globals.backend_url + '/users/'
        await httpHelper.httpGetRequest(apiURL, userId)
    });

When('the administrator sends a user creation request for user {string} password {string} using POST request then response should contain',
    async function (username, password, dataTable) {
        const apiURL = client.globals.backend_url + '/users/'
        // TODO under progress
        const body = {
            'username': 'testnightwatch',
            'password': '12345'
        }
        const status1 = await httpHelper.httpPostRequest(apiURL, body)
    });


When('the HTTP status code should be {string}', function (expectedStatusCode) {
    const lastResponseMeta = httpHelper.getLastResponseMeta()
    return assert.strictEqual(
        lastResponseMeta.status,
        parseInt(expectedStatusCode)
    )
});

When('user {string} should exist', function (username) {
    console.log('pending');
});

Then('response should contain following information', function (dataTable) {
    const expectedUserAttr = dataTable.rowsHash()
    const lastResponse = httpHelper.getLastResponse()
    for (const [key, value] of Object.entries(expectedUserAttr)) {
      assert.strictEqual(
          lastResponse[key].toString(),
          value
      )
    }
});
