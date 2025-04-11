# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pprint
from ..app.main import User
from abc import ABC, abstractmethod
from univention.admin.rest.client import UDM
# from udm_rest_client.udm import UDM


class UsersPort(ABC):
    @abstractmethod
    def list_users(self, query: str) -> list[User]:
        ...


class UDMUsersAdapter(UsersPort):
    def __init__(
        self,
        udm_users_module: UDM.Module,
    ):
        self.module = udm_users_module

    def list_users(self, query: str = "") -> list[User]:
        users = []
        result = self.module.search(
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


class TestUsersAdapter(UsersPort):
    def list_users(self, query: str) -> list[User]:
        users = [
            User(
                username="test01",
                email="test01@example.org",
                firstname="test",
                lastname="test01",
            ),
            User(
                username="test02",
                email="test02@example.org",
                firstname="test",
                lastname="test02",
            ),
        ]
        return users


if __name__ == "__main__":
    udm_test = UDMUsersAdapter(
        uri="http://localhost:9979/udm/",
        username="Administrator",
        password="0ee416b7f0284b0bcc7f146e5e2407a5c8a36200"
    )
    users = udm_test.list_users()
    pprint.pprint(users)
