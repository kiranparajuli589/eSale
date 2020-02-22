const fetch = require('node-fetch')
const {client} = require('nightwatch-api')
let lastResponse = {}
let lastMetaResponse = {}


module.exports = {
    CLIENT_ID: process.env.CLIENT_ID,
    CLIENT_SECRET: process.env.CLIENT_SECRET,
    accessToken: process.env.ACCESS_TOKEN,
    setLastResponse: async (response) => {
      lastResponse = await response.json()
    },
    getLastResponse: () => {
      return lastResponse
    },
    setLastResponseMeta: async (metaResponse) => {
        lastMetaResponse = metaResponse
    },
    getLastResponseMeta: () => {
      return lastMetaResponse
    },
    getOauthHeader: function () {
        return {
            Authorization: "Bearer " + this.accessToken,
        }
    },
    httpGetRequest: async function (apiUrl, pk = null) {
        let url = pk === null ? apiUrl : apiUrl + pk + '/'
        const headers = this.getOauthHeader()
        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        })
        if (!(response["status"] === 200)) {
            throw new Error("Expected response to be success, but got:\n" +
                "status: " + response["status"] + '\n' +
                "error: " + response["statusText"] + '\n' +
                "Full Response: " + response
            )
        }
        this.setLastResponseMeta({
            url: response["url"],
            status: response["status"],
            statusText: response["statusText"],
            headers: response["headers"],
        })
        await this.setLastResponse(response)
    },
    httpPostRequest: async function (url, body) {
        let headers
        headers = this.getOauthHeader()
        const response = await fetch(
            url,
            {
                method: 'POST',
                headers: headers,
                body: {"username": "kirantestni", "password": "kiran"},
            })
        if (!(response["status"] === 200)) {
            throw new Error("Expected response to be success, but got:\n" +
                "status: " + response["status"] + '\n' +
                "error: " + response["statusText"]
            )
        }
        return await JSON.parse(response)
    },
}