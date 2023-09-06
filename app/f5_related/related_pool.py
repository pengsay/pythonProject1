from fastapi import APIRouter, HTTPException
from f5_token import get_token
import f5_related.schemas
from fastapi.encoders import jsonable_encoder
import requests
import json
from f5_related.to_excel import to_excel
from config import Setting
from app_logging import logger

router = APIRouter()
settings = Setting()
root = settings.f5_root


@router.get("/")
def get_pool():
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)['items']
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.post("/to_excel")
def pool_toexcel():
    return to_excel(get_pool())


@router.post("/add_pool")
def add_pool(pool: f5_related.schemas.Pool):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool"
    payload = json.dumps(jsonable_encoder(pool))

    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.post("/vs_to_pool")
def vs_to_pool(partition, vs_name, pool_name):
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition}~{vs_name}"
    token = get_token(root)
    payload = "{\"pool\":\"%s\"}" % pool_name
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.delete("/{pool_name}")
def delete_pool(pool_name):
    url = f"https://{root}/mgmt/tm/ltm/pool/{pool_name}"
    token = get_token(root)
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
        if "code" in response.text:
            raise Exception(response.text)
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.post("/add_member")
def add_menber(partition, pool_name, member_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members"

    payload = "{\"name\":\"%s\"}" % member_name
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        data = json.loads(response.text)
        if "code" in data:
            raise Exception(data)
        return data
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.delete("/delete_members")
def delete_members(root, partition, pool_name, member_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members/{member_name}"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_members")
def get_members(partition, pool_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = json.loads(response.text)
        if "code" in data:
            raise Exception(data)
        return data['items']
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.patch("/stop_member")
def stop_member(partition, pool_name, menber_ip_port):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members/~{partition}~{menber_ip_port}"

    payload = "{\"session\":\"user-disabled\",\"state\":\"user-down\"}"
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.patch("/start_member")
def start_member(partition, pool_name, menber_ip_port):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members/~{partition}~{menber_ip_port}"

    payload = "{\"session\":\"user-enabled\",\"state\":\"user-up\"}"
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_member_data")
def get_member_data(partition, pool_name, menber_ip_port):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/pool/~{partition}~{pool_name}/members/~{partition}~{menber_ip_port}/stats"

    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }


    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
