import json

from fastapi import APIRouter
from f5_related.f5_token import get_token
import requests
from config import Setting
router = APIRouter()
settings = Setting()
root = settings.f5_root

@router.get("/")
def get_rules():


    url = f"https://{root}/mgmt/tm/ltm/rule"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': 'GIZZ2LWNAJIR7YDLVG7SFS54VK'
    }

    response = requests.request("GET", url, headers=headers, data=payload,verify=False)

    return json.loads(response.text)['items']


@router.post("/")
def add_rules( rule_name):
    url = f"https://{root}/mgmt/tm/ltm/rule"
    token = get_token(root)
    payload = "{\n    \"name\":\"%s\"\n}" % rule_name
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return json.loads(response.text)


@router.delete("/")
def add_rules( rule_name):
    url = f"https://{root}/mgmt/tm/ltm/rule/{rule_name}"
    print("_______________________",url)
    token = get_token(root)
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    response = requests.request("DELETE", url, headers=headers, verify=False)

    return response.text
