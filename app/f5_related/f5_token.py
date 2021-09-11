from requests import request
import json
from config import Setting

settings = Setting()

username = settings.f5_username
password = settings.f5_password


def get_token(root):
    print(username, password, settings.f5_root)
    url = f"https://{root}/mgmt/shared/authn/login"

    payload = "{'username': %s, 'password': %s}" % (username, password)
    headers = {
        'Content-Type': 'application/json'
    }
    response = request("POST", url, headers=headers, data=payload, verify=False)
    print(json.loads(response.text))
    token = json.loads(response.text)['token']['token']
    return token
