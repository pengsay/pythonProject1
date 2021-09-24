from fastapi import HTTPException, APIRouter
from config import Setting
from firewall_related.schemas import AddSecurityRule, AddNatRule
import panos
import panos.firewall
import panos.policies
from fastapi.encoders import jsonable_encoder

router = APIRouter()
setting = Setting()

username = setting.fw_username
password = setting.fw_password
root = setting.fw_root


@router.get("/get_security_rule")
def get_security_rule():
    fw = panos.firewall.Firewall(root, api_username=username, api_password=password)
    rulebase = panos.policies.Rulebase()
    fw.add(rulebase)
    current_security_rules = panos.policies.SecurityRule.refreshall(rulebase)
    result = [i.name for i in current_security_rules]
    return result


@router.get("/get_nat_rule")
def get_nat_rule():
    fw = panos.firewall.Firewall(root, api_username=username, api_password=password)
    rulebase = panos.policies.Rulebase()
    fw.add(rulebase)
    current_nat_rules = panos.policies.NatRule.refreshall(rulebase)
    result = [i.name for i in current_nat_rules]
    return result


@router.post("/add_security_rule")
def add_security_rule(desired_rule_params: AddSecurityRule):
    desired_rule_params = jsonable_encoder(desired_rule_params)
    end = {}
    print(type(desired_rule_params))
    for k in desired_rule_params.keys():
        if desired_rule_params[k] != "":
            end[k] = desired_rule_params[k]
    print(end)
    fw = panos.firewall.Firewall(root, api_username=username, api_password=password)
    rulebase = panos.policies.Rulebase()
    fw.add(rulebase)
    current_security_rules = panos.policies.SecurityRule.refreshall(rulebase)
    is_present = False
    print("Current security rule(s) ({0} found):".format(len(current_security_rules)))
    for rule in current_security_rules:
        print("- {0}".format(rule.name))
        if rule.name == end["name"]:
            is_present = True

    if is_present:
        raise HTTPException(status_code=400, detail='Rule "{0}" already exists'.format(end["name"]))

    print('Rule "{0}" not present, adding it'.format(end["name"]))
    new_rule = panos.policies.SecurityRule(**end)

    rulebase.add(new_rule)
    print("Creating rule...")
    new_rule.create()
    print("Done!")
    print("Performing commit...")

    return end
    fw.commit(sync=True)
    print("Done!")


@router.post("/add_nat_rule")
def add_nat_rule(desired_rule_params: AddNatRule):
    desired_rule_params = jsonable_encoder(desired_rule_params)
    end = {}
    print(type(desired_rule_params))
    for k in desired_rule_params.keys():
        if desired_rule_params[k] != "":
            end[k] = desired_rule_params[k]
    print(end)
    fw = panos.firewall.Firewall(root, api_username=username, api_password=password)
    rulebase = panos.policies.Rulebase()
    fw.add(rulebase)
    current_nat_rules = panos.policies.NatRule.refreshall(rulebase)
    is_present = False
    print("Current security rule(s) ({0} found):".format(len(current_nat_rules)))
    for rule in current_nat_rules:
        print("- {0}".format(rule.name))
        if rule.name == end["name"]:
            is_present = True

    if is_present:
        raise HTTPException(status_code=400, detail='Rule "{0}" already exists'.format(end["name"]))

    print('Rule "{0}" not present, adding it'.format(end["name"]))
    new_rule = panos.policies.NatRule(**end)

    rulebase.add(new_rule)
    print("Creating rule...")
    new_rule.create()
    print("Done!")
    print("Performing commit...")

    return end
    fw.commit(sync=True)
    print("Done!")


# @router.delete("/delete_nat_rule")
# def delete_nat_rule(rules_name):
#     fw = panos.firewall.Firewall(root, api_username=username, api_password=password)
#     rulebase = panos.policies.Rulebase()
#     fw.add(rulebase)
#
#     nat = panos.policies.NatRule.refreshall(rulebase)
#     print(type(nat))
#     for i in nat:
#         print(dir(i))
#         if i.name == rules_name:
#             print(i)
#     print(dir(fw))

    # rulebase = panos.policies.Rulebase()
    # fw.add(rulebase)


