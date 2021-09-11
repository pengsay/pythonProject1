import requests
import json
from fastapi import APIRouter
from f5_related.f5_token import get_token
from config import Setting
from f5_related.to_excel import to_excel

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

    virtual_list = json.loads(response.text)['items']
    for i in virtual_list:
        print(type(i))
    end_data = []
    for vs in virtual_list:
        vs_info = []
        result = {
            "name": vs["name"],
            "partition": vs["partition"],
        }
        if 'rulesReference' in vs:
            if type(vs['rulesReference']) == dict:
                irules_url = vs['rulesReference']['link'].replace("localhost", root)
                irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
                print(irules_response)
                irules_info = json.loads(irules_response.text)

                result["rules"] = [{
                    "name": irules_info["name"],
                    "info": irules_info['apiAnonymous']
                }]
            else:
                temp = []
                for j in vs['rulesReference']:
                    irules_url = j['link'].replace("localhost", root)
                    irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
                    irules_info = json.loads(irules_response.text)

                    temp.append({
                        "name": irules_info["name"],
                        "info": irules_info['apiAnonymous']
                    })
                result["rules"] = temp
        # get pool
        if 'poolReference' in vs:
            if type(vs["poolReference"]) == dict:
                pool_url = vs["poolReference"]['link'].replace("localhost", root)
                pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
                pool_info = json.loads(pool_response.text)
                # get members
                members_url = pool_info['membersReference']['link'].replace("localhost", root)
                members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
                members_list = json.loads(members_response.text)["items"]
                end_menber = []
                for i in members_list:
                    temp = {
                        "name": i["name"],
                        "fullPath": i["fullPath"],
                        "session": i["session"],
                        "state": i["state"]
                    }
                    end_menber.append(temp)
                result['pool'] = [{
                    "pool": {
                        "name": pool_info['name'],
                        "monitor": pool_info["monitor"] if "monitor" in pool_info else None,
                        "members": end_menber if "members" in pool_info else None,
                    },
                }]
            else:
                pool_list = []
                for j in vs["poolReference"]:
                    pool_url = j['link'].replace("localhost", root)
                    pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
                    pool_info = json.loads(pool_response.content.decode())
                    # get members
                    members_url = pool_info['membersReference']['link'].replace("localhost", root)
                    members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
                    members_list = json.loads(members_response.content.decode())["items"]
                    end_menber = []
                    for i in members_list:
                        temp = {
                            "name": i["name"],
                            "fullPath": i["fullPath"],
                            "session": i["session"],
                            "state": i["state"]
                        }
                        end_menber.append(temp)
                    pool_list.append({
                        "pool": {
                            "name": pool_info['name'],
                            "monitor": pool_info["monitor"] if "monitor" in pool_info else None,
                            "members": end_menber if "members" in pool_info else None,
                        },
                    })
                result['pool'] = pool_list
        end_data.append(result)
    return end_data


@router.get("/get_virtual/{vs_name}")
def get_virtual(vs_name):
    url = f"https://{root}/mgmt/tm/ltm/pool/"
    vs_list = get_all_virtual()
    payload = {}
    token = get_token(root)

    headers = {
        'X-F5-Auth-Token': token
    }
    # get vs
    vs_info = []
    for i in vs_list:
        if vs_name == i["name"]:
            vs_info.append(i)
    if len(vs_info) != 0:
        irules_info = ''
        vs_info = vs_info[0]
        result = {
            "name": vs_info["name"],
            "partition": vs_info["partition"],
        }
        # get irules
        if 'rulesReference' in vs_info:
            if type(vs_info['rulesReference']) == dict:
                irules_url = vs_info['rulesReference']['link'].replace("localhost", root)
                irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
                irules_info = json.loads(irules_response.content.decode())
                result["rules"] = [{
                    "name": irules_info["name"],
                    "info": irules_info['apiAnonymous']
                }]
            else:
                temp = []
                for j in vs_info['rulesReference']:
                    irules_url = j['link'].replace("localhost", root)
                    irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
                    irules_info = json.loads(irules_response.content.decode())
                    temp.append({
                        "name": irules_info["name"],
                        "info": irules_info['apiAnonymous']
                    })
                result["rules"] = temp

                # get pool
        if 'poolReference' in vs_info:
            if type(vs_info["poolReference"]) == dict:
                pool_url = vs_info["poolReference"]['link'].replace("localhost", root)
                pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
                pool_info = json.loads(pool_response.content.decode())
                # get members

                members_url = pool_info['membersReference']['link'].replace("localhost", root)
                members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
                members_list = json.loads(members_response.content.decode())["items"]

                end_menber = []
                for i in members_list:
                    temp = {
                        "name": i["name"],
                        "fullPath": i["fullPath"],
                        "session": i["session"],
                        "state": i["state"]
                    }
                    end_menber.append(temp)
                result['pool'] = [{
                    "pool": {
                        "name": pool_info['name'],
                        "monitor": pool_info["monitor"],
                        "members": end_menber
                    },
                }]
            else:
                temp = []
                for j in vs_info["poolReference"]:
                    pool_url = j['link'].replace("localhost", root)
                    pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
                    pool_info = json.loads(pool_response.content.decode())
                    # get members

                    members_url = pool_info['membersReference']['link'].replace("localhost", root)
                    members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
                    members_list = json.loads(members_response.content.decode())["items"]

                    end_menber = []
                    for i in members_list:
                        temp = {
                            "name": i["name"],
                            "fullPath": i["fullPath"],
                            "session": i["session"],
                            "state": i["state"]
                        }
                        end_menber.append(temp)
                    temp.append({
                        "pool": {
                            "name": pool_info['name'],
                            "monitor": pool_info["monitor"],
                            "members": end_menber
                        },
                    })
                result['pool'] = temp
        return result
    else:
        return "vs不存在"


@router.post("/vs_toexcel")
def vs_to_excel():
    data = get_all_virtual()
    end = []
    for i in data:

        temp = {
            "name": i['name'],
            "rules_name": [j['name'] for j in i['rules']] if 'rules' in i else None,
            "rules": [j['info'] for j in i['rules']] if 'rules' in i else None,
            "pool_name":[j["pool"]["name"] for j in i["pool"]] if "pool" in i else None,
            "pool_member":[j["pool"]["members"] for j in i["pool"]] if "pool" in i else None,
            "monitor":[j["pool"]["monitor"] for j in i["pool"]] if "pool" in i else None,
            "partition":i["partition"]}
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

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.text


@router.delete("/{vs_name}")
def delete_vs(vs_name):
    token = get_token(root)
    url = f"https://172.16.66.153/mgmt/tm/ltm/virtual/{vs_name}"
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, verify=False)
    return response.text


@router.patch("/stop/{partition_name}/{listener_name}")
def stop_vs(partition_name, listener_name):
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition_name}~{listener_name}"

    payload = '{"disabled": true}'
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': 'PADPHFB45VKMI4DCZPS3JC3DYR'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    if response.text == None:
        return {
            "status": 203,
            "info": "删除成功"
        }
    return response.text


@router.patch("/start/{partition_name}/{listener_name}")
def start_vs(partition_name, listener_name):
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition_name}~{listener_name}"

    payload = '{"enabled": true}'
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': 'PADPHFB45VKMI4DCZPS3JC3DYR'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)

    return response.text


@router.get("/get_stats")
def get_stats(partition, vs_name):
    token = get_token(root)
    url = f"https://{root}/mgmt/tm/ltm/virtual/~{partition}~{vs_name}/stats"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    data = json.loads(response.text)

    return data
