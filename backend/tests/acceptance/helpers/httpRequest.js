const fetch = require('node-fetch')
const {client} = require('nightwatch-api')


module.exports = {
    CLIENT_ID: process.env.CLIENT_ID,
    CLIENT_SECRET: process.env.CLIENT_SECRET,
    accessToken: process.env.ACCESS_TOKEN,
    getOauthHeader: function () {
        return {
            Authorization: "Bearer " + this.accessToken,
            ContentTypes: "application/json",
            Accept: "application/json",
            // ContentEncoding: "utf-8"
        }
    },
    httpGetRequest: async function (apiUrl, pk = null) {
        let url = pk === null ? apiUrl : apiUrl + pk + '/'
        const headers = this.getOauthHeader()
        const response = await fetch(
             url,
            {
                  method: 'GET',
                  headers: headers
            })
        if (!(response.status === 200)) {
            throw new Error("Expected response to be success, but got:\n" +
                "status: " + response.status + '\n' +
                "error: " + response.statusText
            )
        }
        return await response.json()
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
        if (!(response.status === 200)) {
            throw new Error("Expected response to be success, but got:\n" +
                "status: " + response.status + '\n' +
                "error: " + response.statusText
            )
        }
        return await JSON.parse(response)
    },
}