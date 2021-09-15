import json

from fastapi import APIRouter, HTTPException
from f5_token import get_token
import requests
from config import Setting
from app_logging import logger

router = APIRouter()
settings = Setting()
root = settings.f5_root


@router.get("/")
def get_rules():
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/rule"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': "123123123123123123"
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = json.loads(response.text)
        if data["code"]:
            raise Exception(response.text)
        return data['items']
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.post("/")
def add_rules(rule_name):
    url = f"https://{root}/mgmt/tm/ltm/rule"
    token = get_token(root)
    payload = "{\n    \"name\":\"%s\"\n}" % rule_name
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        if json.loads(response.text)["code"]:
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.delete("/")
def delete_rules(rule_name):
    url = f"https://{root}/mgmt/tm/ltm/rule/{rule_name}"
    print("_______________________", url)
    token = get_token(root)
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }
    try:
        response = requests.request("DELETE", url, headers=headers, verify=False)
        if json.loads(response.text)["code"]:
            raise Exception(response.text)

        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
