# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
from keycloak import KeycloakOpenIDConnection, KeycloakAdmin
from abc import ABC, abstractmethod


class TwoFAPort(ABC):
    @abstractmethod
    def reset_token(self, username: str) -> None:
        ...


class KeycloakTwoFAAdapter(TwoFAPort):
    def __init__(
        self,
        server_url: str,
        client_id: str,
        realm_name: str,
        client_secret: str,
    ):
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
            client_secret_key=client_secret,
        )
        self.keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

    def reset_token(self, username: str) -> None:
        user_id = self.keycloak_admin.get_user_id(username)
        credentials = self.keycloak_admin.get_credentials(user_id=user_id)
        otp_creds = [i for i in credentials if i["type"] == "otp"]  # filter OTPs from credentials
        for cred in otp_creds:
            self.keycloak_admin.delete_credential(user_id=user_id, credential_id=cred["id"])


class TestTwoFAAdapter(TwoFAPort):
    def reset_token(self, username: str):
        return


if __name__ == "__main__":
    # server_url = os.environ("KEYCLOAK_SERVER_URL")
    # client_id = os.environ("KEYCLOAK_CLIENT_ID")
    # realm_name = os.environ("KEYCLOAK_REALM_NAME")
    # client_secret = os.environ("KEYCLOAK_CLIENT_SECRET")
    two_fa_test = KeycloakTwoFAAdapter(
        server_url="https://id.jahlers-opendesk.univention.dev",
        client_id="resttest",
        realm_name="opendesk",
        client_secret="sHYYBqgsVHr2mHDsG2PzhRYzesQqjLPr"
    )
    two_fa_test.reset_token("test02")
