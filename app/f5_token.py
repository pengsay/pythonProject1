from fastapi import HTTPException
from requests import request
import json
from config import Setting
from app_logging import logger

settings = Setting()

username = settings.f5_username
password = settings.f5_password
# password = '12345'


def get_token(root):
    url = f"https://{root}/mgmt/shared/authn/login"

    payload = "{'username': %s, 'password': %s}" % (username, password)
    headers = {
        'Content-Type': 'application/json'
    }
    response = request("POST", url, headers=headers, data=payload, verify=False)
    try:
        token = json.loads(response.text)['token']['token']
        return token
    except Exception as e:

        logger.error(response.text)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


