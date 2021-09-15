from f5_token import get_token
from config import Setting
import json
from app_logging import logger
from fastapi import HTTPException, APIRouter
from dns_related.schemas import WideCreate, UpdateWideIp
from fastapi.encoders import jsonable_encoder

import requests

setting = Setting()
root = setting.f5_root
router = APIRouter()


@router.get("/get_vs")
def get_all_vs():
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/gtm/server"

    payload = {}
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
    vs_info = []
    for server in json.loads(response.text)['items']:
        server_url = server["virtualServersReference"]["link"].replace("localhost", root)
        server_fullPath = server["fullPath"]
        server_response = requests.request("GET", server_url, headers=headers, data=payload, verify=False)
        vs_list = json.loads(server_response.text)["items"]
        for vs in vs_list:
            temp = server_fullPath + ":" + vs["fullPath"]
            vs_info.append(temp)

    return vs_info


@router.post("/create_pool")
def create_pool(pool_name, members, partition):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/gtm/pool/a"
    payload = '{"name":"%s","members":"%s","partition": "%s"}' % (pool_name, members, partition)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_pools")
def get_pools():
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/gtm/pool/a"
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)['items']
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.post("/create_wideip")
def create_wideip(wide: WideCreate):
    url = f"https://{root}/mgmt/tm/gtm/wideip/a"

    token = get_token(root)
    payload = json.dumps(jsonable_encoder(wide))
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.delete("/delete_wideip")
def delete_wideip(partition, wideip_name):
    url = f" https://{root}/mgmt/tm/gtm/wideip/a/~{partition}~{wideip_name}"
    token = get_token(root)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("DELETE", url, headers=headers, verify=False)
        if "code" in response.text:
            raise Exception(response.text)
        return {
            "info": "删除成功"
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_wideip")
def get_wideip():
    url = f" https://{root}/mgmt/tm/gtm/wideip/a"
    token = get_token(root)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(response.text)
        return json.loads(response.text)['items']
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_a_wideip")
def get_a_wideip(partition, wideip_name):
    url = f" https://{root}/mgmt/tm/gtm/wideip/a/~{partition}~{wideip_name}"
    token = get_token(root)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(response.text)
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.put("/update_wideip")
def update_wideip(partition, wideip_name, pools: UpdateWideIp):
    url = f"https://{root}/mgmt/tm/gtm/wideip/a/~{partition}~{wideip_name}"
    try:
        wideip = get_a_wideip(partition, wideip_name)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
    wideip = jsonable_encoder(wideip)
    pools = [jsonable_encoder(i) for i in jsonable_encoder(pools)["pools"]]
    try:
        wideip["pools"] = pools
        wideip.pop("kind")
        for key in wideip:
            if wideip[key] == "":
                wideip[key] = "none"
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")

    payload = json.dumps(wideip)
    print(payload)
    token = get_token(root)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        print(response.text)
        if "code" in json.loads(response.text):
            raise Exception(response.text)
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_dns_a")
def get_dns_a(partition, wideip_name):
    token = get_token(root)
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        wideip = get_a_wideip(partition, wideip_name)
        pools = wideip["pools"]
        pool_urls = [i["nameReference"]["link"].replace("localhost", root) for i in pools]
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
    result = []
    for pool_url in pool_urls:
        try:
            response = requests.request("GET", pool_url, headers=headers, verify=False)
            if "code" in json.loads(response.text):
                raise Exception(json.loads(response.text))
            temp = json.loads(response.text)["membersReference"]
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail="请求有误稍后重试")
        member_url = []
        if type(temp) == dict:
            member_url.append(temp["link"].replace("localhost", root))
        elif type(temp) == list:
            member_url = [i["link"].replace("localhost", root) for i in temp]

        for url in member_url:
            try:
                response = requests.request("GET", url, headers=headers, verify=False)
                if "code" in json.loads(response.text):
                    raise Exception(json.loads(response.text))
                print(json.loads(response.text))
                members = json.loads(response.text)['items']
                for member in members:
                    result.append(member["fullPath"])
            except Exception as e:
                logger.error(e)
                raise HTTPException(status_code=400, detail="请求有误稍后重试")
    return result
