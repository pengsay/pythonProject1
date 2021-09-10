import json

from user_related import models
from fastapi import Depends
from fastapi_permissions import (
    Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    All,
)
from user_related.get_token import get_current_user

user_acl_list = [
    (Allow, Everyone, "show"),
    (Allow, "role:admin", All),
]


def get_active_principals(user: models.User = Depends(get_current_user)):
    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(json.loads(user.principals))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals


Permission = configure_permissions(get_active_principals)
