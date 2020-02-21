const chromedriver = require('chromedriver')
const withHttp = url => /^https?:\/\//i.test(url) ? url : `http://${url}`

const ESALE_BACKEND_URL = withHttp(process.env.ESALE_SERVER_BACKEND_URL || 'http://127.0.0.1:8888')
const LOCAL_LAUNCH_URL = withHttp(process.env.ESALE_SERVER_LAUNCH_URL || 'http://127.0.0.1:8888')
const ESALE_ADMIN_USERNAME = process.env.ESALE_BACKEND_USERNAME || 'admin'
const ESALE_ADMIN_PASSWORD = process.env.ESALE_BACKEND_PASSWORD || 'admin'
const SELENIUM_HOST = process.env.SELENIUM_HOST || '127.0.0.1'
const BROWSER_NAME = process.env.BROWSER_NAME


module.exports = {
    src_folders: ['tests'],
    page_objects_path: './tests/acceptance/pageObjects',
    webdriver: {
      start_process: true,
      server_path: chromedriver.path,
      cli_args: [
        "--verbose"
      ],
      port: 9515
    },
    test_settings: {
        default: {
          selenium_host: SELENIUM_HOST,
          launch_url: "https://www.google.com",
          globals: {
            waitForConditionTimeout: 20000,
            waitForConditionPollInterval: 10,
            backend_url: ESALE_BACKEND_URL,
            backend_admin_username: ESALE_ADMIN_USERNAME,
            backend_admin_password: ESALE_ADMIN_PASSWORD,
          },
          desiredCapabilities: {
                browserName: BROWSER_NAME || 'chrome',
                javascriptEnabled: true,
                chromeOptions: {
                    args: ['disable-gpu'],
                    w3c: false
                }
            }
        }
    }
};