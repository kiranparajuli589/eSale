const fetch = require('node-fetch')
const {client} = require('nightwatch-api')
const axios = require('axios');
let lastResponse = {}
let lastMetaResponse = {}
let accessToken = ""


module.exports = {
    setLastResponse: async (response) => {
        lastResponse = await response.json()
    },
    getLastResponse: () => {
        return lastResponse
    },
    setLastResponseMeta: function (metaResponse) {
        lastMetaResponse = metaResponse
    },
    getLastResponseMeta: () => {
        return lastMetaResponse
    },
    getNewAccessToken: async function () {
        const url = "http://127.0.0.1:8888/auth/token"
        const response = await axios.post(url,
                                "client_id=" + process.env.CLIENT_ID + '&' +
                    "client_secret=" + process.env.CLIENT_SECRET + '&' +
                    "grant_type=password" + '&' +
                    "username=admin" + '&' +
                    "password=admin"
        )
        console.log(response)
        accessToken = response["data"]["access_token"]
    },
    getAccessToken: async function () {
        if (accessToken === '')
            await this.getNewAccessToken()
        return accessToken
    },
    getOauthHeader: async function () {
        accessToken = await this.getAccessToken()
        return {
            Authorization: "Bearer " + accessToken,
        }
    },
    setResponse: async function (response) {
        const metaResponse = {
            url: response["url"],
            status: response["status"],
            statusText: response["statusText"],
            headers: response["headers"],
        }
        this.setLastResponseMeta(metaResponse)
        await this.setLastResponse(response)
    },
    httpGetRequest: async function (apiUrl, pk = null) {
        let url = pk === null ? apiUrl : apiUrl + pk + '/'
        const headers = await this.getOauthHeader()
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
        await this.setResponse(response)
    },
    httpPostRequest: async function (url, body) {
        let headers
        headers = this.getOauthHeader()
        const response = await fetch(
            url,
            {
                method: 'POST',
                headers: headers,
                body: body,
            })
        if (!(response["status"] === 200)) {
            throw new Error("Expected response to be success, but got:\n" +
                "status: " + response["status"] + '\n' +
                "error: " + response["statusText"]
            )
        }
        await this.setResponse(response)
    },
}