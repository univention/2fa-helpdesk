# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from dataclasses import dataclass
from ..adapters.users import UsersPort, UDMUsersAdapter
from ..adapters.auth import AuthPort, UDMAuthAdapter
from ..adapters.two_fa import TwoFAPort, KeycloakTwoFAAdapter
from ..adapters.api import APIPort


@dataclass
class User:
    username: str
    email: str
    firstname: str
    lastname: str


class App(APIPort):
    def __init__(self, users: UsersPort, auth: AuthPort, two_fa: TwoFAPort):
        self.users = users
        self.auth = auth
        self.two_fa = two_fa

    # @property
    # def auth(self) -> AuthPort:
    #     ...

    def reset_own_token(self) -> None:
        self.two_fa.reset_token(self.auth.username)

    def reset_user_tokens(self, usernames: list[str]) -> None:
        if self.auth.is_2fa_admin():
            for username in usernames:
                self.two_fa.reset_token(username)

    def list_users(self, query: str) -> list[dict]:
        if self.auth.is_2fa_admin():
            return self.users.list_users(query)
