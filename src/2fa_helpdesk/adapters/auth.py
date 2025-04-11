# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from abc import ABC, abstractmethod
from univention.admin.rest.client import UDM
# from udm_rest_client.udm import UDM


class AuthPort(ABC):
    @abstractmethod
    def is_2fa_admin(self, username: str) -> bool:
        ...


class UDMAuthAdapter(AuthPort):
    def __init__(
        self,
        udm_users_module: UDM.Module,
    ):
        self.module = udm_users_module

    def is_2fa_admin(self, username: str) -> bool:
        obj = next(self.module.search(f'uid={username}'))
        obj = obj.open()
        groups = obj.properties.groups
        if self.two_fa_admin_group_dn in groups:
            return True
        else:
            return False
