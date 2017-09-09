import datetime

from logger import logger

log = logger().log


class Login:
    def __init__(self, req):
        self.req = req

    def login(self, account):
        nikeLoginHeader = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 5.1.1; KFFOWI Build/LVY48F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36"
        }

        email = account.split(':')[0]
        password = account.split(':')[1]


        self.req.headers.update(nikeLoginHeader)
        loginData = {
	        "username"       : email,
	        "password"       : password,
	        "keepMeLoggedIn" : "true",
	        "client_id"      : "rljauGDgy7n9ZSEeFDBDLmA4BAvuf9Ff",
	        "ux_id"          : "com.nike.commerce.omega.test",
	        "grant_type"     : "password"
        }

        while True:
            login = self.req.post(
                "https://unite.nikecloud.com/login?appVersion=281&experienceVersion=244&uxid=com.nike.commerce.snkrs.ios&locale=en_US&backendEnvironment=identity&browser=Apple+Computer%2C+Inc.&os=undefined&mobile=true&native=true",
                json=loginData)
            if login.status_code == 200:
                break
            else:
                log(login.json()["error_description"], "error")
                return True
        access_token = login.json()['access_token']

        url = "https://api.nike.com/plus/v3/notifications/me/stored?before={}Z&locale=en_US&limit=20".format(datetime.datetime.now().isoformat())

        headers = {
            "authorization" : "Bearer {}".format(access_token)
        }
        messages = self.req.get(url, headers = headers)

        if len(messages.json()['notifications']) == 0:
            log("Empty Inbox", "error")
        else:
            for i in messages.json()['notifications']:
                log(i['message'].encode("utf8"))


        return True