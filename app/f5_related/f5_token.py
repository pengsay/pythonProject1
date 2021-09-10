from requests import request
import json
from config import Setting

settings = Setting()

username = settings.username
password = settings.password


def get_token(root):
    url = f"https://{root}/mgmt/shared/authn/login"

    payload = "{'username': %s, 'password': %s}" % (username, password)
    headers = {
        'Content-Type': 'application/json'
    }
    response = request("POST", url, headers=headers, data=payload, verify=False)

    token = json.loads(response.text)['token']['token']
    return token
