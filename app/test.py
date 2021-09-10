import requests
import json

root = "172.16.66.153"
username = 'admin'
password = "1qaz@WSX3edc$RFV"


def get_token(root):
    url = f"https://{root}/mgmt/shared/authn/login"

    payload = "{'username': %s, 'password': %s}" % (username, password)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    token = json.loads(response.text)['token']['token']
    return token


def get_all_virtual(root):
    url = f"https://{root}/mgmt/tm/ltm/virtual"
    token = get_token(root)
    payload = {}
    headers = {
        'X-F5-Auth-Token': token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    virtual_list = json.loads(response.text)['items']

    return virtual_list


def get_virtual(vs_name, root):
    url = f"https://{root}/mgmt/tm/ltm/pool/"
    vs_list = get_all_virtual(root)
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
            irules_url = vs_info[0]['rulesReference']['link'].replace("localhost", root)
            irules_response = requests.request("GET", irules_url, headers=headers, data=payload, verify=False)
            irules_info = json.loads(irules_response.content.decode())
            result["rules"] = {
                "name": irules_info["name"],
                "info": irules_info['apiAnonymous']
            }
        # get pool
        if 'poolReference' in vs_info:
            pool_url = vs_info["poolReference"]['link'].replace("localhost", root)
            pool_response = requests.request("GET", pool_url, headers=headers, data=payload, verify=False)
            pool_info = json.loads(pool_response.content.decode())
            # get members

            members_url = pool_info['membersReference']['link'].replace("localhost", root)
            members_response = requests.request("GET", members_url, headers=headers, data=payload, verify=False)
            members_list = json.loads(members_response.content.decode())["items"]

            end_menber = []
            for i in members_list:
                dict = {
                    "name": i["name"],
                    "fullPath": i["fullPath"],
                    "session": i["session"],
                    "state": i["state"]
                }
                end_menber.append(dict)
            result['pool'] = {
                "pool": {
                    "name": pool_info['name'],
                    "monitor": pool_info["monitor"],
                    "members": end_menber
                },
            }

        return result
    else:
        return "vs不存在"


def delete_vs(root, vs_name):
    token = get_token(root)
    url = f"https://172.16.66.153/mgmt/tm/ltm/virtual/{vs_name}"
    headers = {
        'X-F5-Auth-Token': token,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, verify=False)
    return {
        "status": 203,
        "info": "删除成功"
    }


print(delete_vs("172.16.66.153", "test1"))
