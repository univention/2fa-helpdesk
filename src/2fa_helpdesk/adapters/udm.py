# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import dataclasses
import os
from univention.admin.rest.client import UDM
import typing

@dataclasses.dataclass
class User:
    username: typing.Optional[str]
    email: typing.Optional[str]
    firstname: typing.Optional[str]
    lastname: typing.Optional[str]

def _get_udm_module(udm_module: str = "users/user"):
    
    username = os.environ["UDM_USERNAME"]
    password = os.environ["UDM_PASSWORD"]
    hostname = os.environ["UDM_HOST"]

    udm_module = UDM.http(hostname, username, password)
    return udm_module

def is_2fa_admin(username: str) -> bool:
    '''Check if a given user is a 2FA-Admin'''

    udm_module = _get_udm_module()
    obj = next(udm_module.module.search(f'uid={username}'))
    obj = obj.open()
    groups = obj.properties.groups
    if udm_module.two_fa_admin_group_dn in groups:
        return True
    else:
        return False

def list_users(query: str = "") -> list[User]:
    '''List users based on a query'''

    users = []
    udm_module = _get_udm_module()
    result = udm_module.module.search(
        f"(|(uid={query}*)(mailPrimaryAddress={query}*)(firstname={query}*)(lastname={query}*))"
    )

    for _user in result:
        _user = _user.open()
        users.append(User(
            username=_user.properties.get("username"),
            email=_user.properties.get("mailPrimaryAddress"),
            firstname=_user.properties.get("firstname"),
            lastname=_user.properties.get("lastname"),
        ))

    return users