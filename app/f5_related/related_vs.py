import requests
import json
from fastapi import APIRouter
from f5_token import get_token
from config import Setting
from f5_related.to_excel import to_excel
from fastapi import HTTPException
from app_logging import logger

router = APIRouter()
settings = Setting()
root = settings.f5_root


@router.get("/get_virtual/")
def get_all_virtual():
    url = f"https://{root}/mgmt/tm/ltm/virtual"
    token = get_token(root)
    payload = {}
    headers = {
        'X-F5-Auth-Token': token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    try:
        virtual_list = json.loads(response.text)['items']
    except Exception as e:

        logger.error(response.text)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")

    for i in virtual_list:
        print(type(i))
    end_data = []
    for vs in virtual_list:
        result = {
            "name": vs["name"],
            "partition": vs["partition"],
        }
        if 'rulesReference' in vs:
            if type(vs['rulesReference']) == dict:
                irules_url = vs['rulesReference']['link'].replace("localhost", root)

                try:
                    irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
                    if "code" in json.loads(irules_response.content.decode()):
                        raise Exception(json.loads(irules_response.content.decode()))
                    irules_info = json.loads(irules_response.content.decode())
                except Exception as e:
                    logger.error(e)
                    raise HTTPException(status_code=400, detail="请求有误稍后重试")

                result["rules"] = [{
                    "name": irules_info["name"],
                    "info": irules_info['apiAnonymous']
                }]
            else:
                temp = []
                for j in vs['rulesReference']:
                    irules_url = j['link'].replace("localhost", root)

                    try:
                        irules_response = requests.request("GET", irules_url, headers=headers, data=payload,
                                                           verify=False)
                        if 'code' in json.loads(irules_response.content.decode()):
                            raise Exception(json.loads(irules_response.content.decode()))
                        irules_info = json.loads(irules_response.content.decode())
                    except Exception as e:
                        logger.error(e)
                        raise HTTPException(status_code=400, detail="请求有误稍后重试")

                    temp.append({
                        "name": irules_info["name"],
                        "info": irules_info['apiAnonymous']
                    })
                result["rules"] = temp
        # get pool
        if 'poolReference' in vs:
            if type(vs["poolReference"]) == dict:
                pool_url = vs["poolReference"]['link'].replace("localhost", root)

                try:
                    pool_response = requests.request("GET", pool_url, headers=headers, verify=False)
                    if "code" in json.loads(pool_response.text):
                        raise Exception(json.loads(pool_response.text))
                    pool_info = json.loads(pool_response.text)
                except Exception as e:
                    logger.error(e)
                    raise HTTPException(status_code=400, detail="请求有误稍后重试")
                # get members
                end_member = []
                if "membersReference" in pool_info:
                    members_url = pool_info['membersReference']['link'].replace("localhost", root)

                    try:
                        members_response = requests.request("GET", members_url, headers=headers, data=payload,
                                                            verify=False)
                        if "code" in json.loads(members_response.text):
                            raise Exception(json.loads(members_response.text))
                        members_list = json.loads(members_response.text)["items"]
                    except Exception as e:
                        logger.error(e)
                        raise HTTPException(status_code=400, detail="请求有误稍后重试")

                    for i in members_list:
                        temp = {
                            "name": i["name"],
                            "fullPath": i["fullPath"],
                            "session": i["session"],
                            "state": i["state"]
                        }
                        end_member.append(temp)
                result['pool'] = [{
                    "pool": {
                        "name": pool_info['name'],
                        "monitor": pool_info["monitor"] if "monitor" in pool_info else None,
                        "members": end_member,
                    },
                }]
            else:
                pool_list = []
                for j in vs["poolReference"]:
                    pool_url = j['link'].replace("localhost", root)

                    try:
                        pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
                        if "code" in json.loads(pool_response.content.decode()):
                            raise Exception(json.loads(pool_response.content.decode()))
                        pool_info = json.loads(pool_response.content.decode())
                    except Exception as e:
                        logger.error(e)
                        raise HTTPException(status_code=400, detail="请求有误稍后重试")
                    # get members
                    members_url = pool_info['membersReference']['link'].replace("localhost", root)

                    try:
                        members_response = requests.request("GET", members_url, headers=headers, data=payload,
                                                            verify=False)
                        if "code" in json.loads(members_response.content.decode()):
                            raise Exception(json.loads(members_response.content.decode()))
                        members_list = json.loads(members_response.content.decode())["items"]
                    except Exception as e:
                        logger.error(e)
                        raise HTTPException(status_code=400, detail="请求有误稍后重试")
                    end_member = []
                    for i in members_list:
                        temp = {
                            "name": i["name"],
                            "fullPath": i["fullPath"],
                            "session": i["session"],
                            "state": i["state"]
                        }
                        end_member.append(temp)
                    pool_list.append({
                        "pool": {
                            "name": pool_info['name'],
                            "monitor": pool_info["monitor"] if "monitor" in pool_info else None,
                            "members": end_member if "members" in pool_info else None,
                        },
                    })
                result['pool'] = pool_list
        end_data.append(result)
    return end_data


# @router.get("/get_virtual/{vs_name}")
# def get_virtual(vs_name):
#     url = f"https://{root}/mgmt/tm/ltm/pool/"
#     vs_list = get_all_virtual()
#     payload = {}
#     token = get_token(root)
#
#     headers = {
#         'X-F5-Auth-Token': token
#     }
#     # get vs
#     vs_info = []
#     for i in vs_list:
#         if vs_name == i["name"]:
#             vs_info.append(i)
#     if len(vs_info) != 0:
#         irules_info = ''
#         vs_info = vs_info[0]
#         result = {
#             "name": vs_info["name"],
#             "partition": vs_info["partition"],
#         }
#         # get irules
#         if 'rulesReference' in vs_info:
#             if type(vs_info['rulesReference']) == dict:
#                 irules_url = vs_info['rulesReference']['link'].replace("localhost", root)
#
#                 try:
#                     irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
#                     if "code" in json.loads(irules_response.content.decode()):
#                         raise Exception(irules_response.content.decode())
#                     irules_info = irules_response.content.decode()
#                 except Exception as e:
#                     logger.error(e)
#                     raise HTTPException(status_code=400, detail="请求有误稍后重试")
#                 result["rules"] = [{
#                     "name": irules_info["name"],
#                     "info": irules_info['apiAnonymous']
#                 }]
#             else:
#                 temp = []
#                 for j in vs_info['rulesReference']:
#                     irules_url = j['link'].replace("localhost", root)
#                     irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
#                     try:
#                         irules_info = json.loads(irules_response.content.decode())
#                     except Exception as e:
#                         logger.error(irules_response.content)
#                         raise HTTPException(status_code=400, detail="请求有误稍后重试")
#                     temp.append({
#                         "name": irules_info["name"],
#                         "info": irules_info['apiAnonymous']
#                     })
#                 result["rules"] = temp
#
#                 # get pool
#         if 'poolReference' in vs_info:
#             if type(vs_info["poolReference"]) == dict:
#                 pool_url = vs_info["poolReference"]['link'].replace("localhost", root)
#
#                 try:
#                     pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
#                     if "code" in json.loads(pool_response.content.decode()):
#                         raise Exception(json.loads(pool_response.content.decode()))
#                     pool_info = json.loads(pool_response.content.decode())
#                 except Exception as e:
#                     logger.error(e)
#                     raise HTTPException(status_code=400, detail="请求有误稍后重试")
#                 # get members
#
#                 members_url = pool_info['membersReference']['link'].replace("localhost", root)
#
#                 try:
#                     members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
#                     if json.loads(members_response.content.decode())['code']:
#                         raise Exception(json.loads(members_response.content.decode()))
#                     members_list = json.loads(members_response.content.decode())["items"]
#                 except Exception as e:
#                     logger.error(e)
#                     raise HTTPException(status_code=400, detail="请求有误稍后重试")
#
#                 end_menber = []
#                 for i in members_list:
#                     temp = {
#                         "name": i["name"],
#                         "fullPath": i["fullPath"],
#                         "session": i["session"],
#                         "state": i["state"]
#                     }
#                     end_menber.append(temp)
#                 result['pool'] = [{
#                     "pool": {
#                         "name": pool_info['name'],
#                         "monitor": pool_info["monitor"],
#                         "members": end_menber
#                     },
#                 }]
#             else:
#                 temp = []
#                 for j in vs_info["poolReference"]:
#                     pool_url = j['link'].replace("localhost", root)
#
#                     try:
#                         pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
#                         if "code" in json.loads(pool_response.content.decode()):
#                             raise Exception(json.loads(pool_response.content.decode()))
#                         pool_info = json.loads(pool_response.content.decode())
#                     except Exception as e:
#                         logger.error(e)
#                         raise HTTPException(status_code=400, detail="请求有误稍后重试")
#                     # get members
#
#                     members_url = pool_info['membersReference']['link'].replace("localhost", root)
#
#                     try:
#                         members_response = requests.request("GET", members_url, headers=headers, data=payload,
#                                                             verify=False)
#                         if "code" in json.loads(members_response.content.decode()):
#                             raise Exception(json.loads(members_response.content.decode()))
#                         members_list = json.loads(members_response.content.decode())["items"]
#                     except Exception as e:
#                         logger.error(e)
#                         raise HTTPException(status_code=400, detail="请求有误稍后重试")
#
#                     end_menber = []
#                     for i in members_list:
#                         temp = {
#                             "name": i["name"],
#                             "fullPath": i["fullPath"],
#                             "session": i["session"],
#                             "state": i["state"]
#                         }
#                         end_menber.append(temp)
#                     temp.append({
#                         "pool": {
#                             "name": pool_info['name'],
#                             "monitor": pool_info["monitor"],
#                             "members": end_menber
#                         },
#                     })
#                 result['pool'] = temp
#         return result
#     else:
#         return "vs不存在"


@router.post("/vs_toexcel")
def vs_to_excel():
    data = get_all_virtual()
    end = []
    for i in data:
        temp = {
            "name": i['name'],
            "rules_name": [j['name'] for j in i['rules']] if 'rules' in i else None,
            "rules": [j['info'] for j in i['rules']] if 'rules' in i else None,
            "pool_name": [j["pool"]["name"] for j in i["pool"]] if "pool" in i else None,
            "pool_member": [j["pool"]["members"] for j in i["pool"]] if "pool" in i else None,
            "monitor": [j["pool"]["monitor"] for j in i["pool"]] if "pool" in i else None,
            "partition": i["partition"]}
        end.append(temp)
    return to_excel(end)


@router.post("/")
def add_virtual(name, destination, profiles="/Common/fastL4", sat_type=None, sat_pool=None):
    url = f"https://{root}/mgmt/tm/ltm/virtual"
    token = get_token(root)
    if sat_type and sat_pool == None:
        payload = json.dumps({"name": name, "destination": destination, "ipProtocol": 'tcp', "profiles": profiles})
    else:
        payload = json.dumps({"name": name, "destination": destination, "ipProtocol": 'tcp', "profiles": profiles,
                              "sourceAddressTranslation": {"type": sat_type, "pool": sat_pool}})
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print("res:",response.text)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.delete("/{vs_name}")
def delete_vs(vs_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/virtual/{vs_name}"
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("DELETE", url, headers=headers, verify=False)
        if "code" in response.text:
            raise Exception(response.text)
        return {"info": "删除成功"}
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.patch("/stop/{partition_name}/{listener_name}")
def stop_vs(partition_name, listener_name):
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition_name}~{listener_name}"
    token = get_token(root)
    payload = '{"disabled": true}'
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }
    try:
        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)

        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return {
            "info": "修改成功"
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.patch("/start/{partition_name}/{listener_name}")
def start_vs(partition_name, listener_name):
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition_name}~{listener_name}"
    token = get_token(root)
    payload = '{"enabled": true}'
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }
    try:
        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
        if "code" in json.loads(response.text):
            raise Exception(json.loads(response.text))
        return {"info": "修改成功"}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")


@router.get("/get_stats")
def get_stats(partition, vs_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition}~{vs_name}/stats"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        data = json.loads(response.text)
        print(data)
        if "code" in data:
            raise Exception(data)
        return data
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="请求有误稍后重试")
