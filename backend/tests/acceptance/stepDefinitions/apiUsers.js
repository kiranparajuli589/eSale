const { Given, When, Then } = require('cucumber');
const { client } = require('nightwatch-api');

Given('this prints {string} in console', function (string) {
    console.log(string)
});

Given('browser browses to {string}', function (string) {
    client.url(string)
});


