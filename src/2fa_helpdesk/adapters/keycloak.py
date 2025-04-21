# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
import keycloak
import fastapi

def _get_kc_admin():
    try:
        kc_admin = keycloak.KeycloakAdmin(
            server_url=os.environ["KEYCLOAK_URL"],
            username=os.environ["KEYCLOAK_USERNAME"],
            password=os.environ["KEYCLOAK_PASSWORD"],
            realm_name=os.environ["KEYCLOAK_REALM_NAME"],
            client_id=os.environ.get("KEYCLOAK_CLIENT_ID") or "admin-cli",
            verify=os.environ.get("KEYCLOAK_VERIFY_SSL") or True
        )
        return kc_admin
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Keycloak connection error: {str(e)}")

def reset_2fa_token(self, username: str) -> dict:
    '''Reset the 2FA token for the give user'''

    kc_admin = _get_kc_admin()

    user_id = kc_admin.get_user_id(username)
    credentials = kc_admin.get_credentials(user_id=user_id)
    
    otp_creds = [i for i in credentials if i["type"] == "otp"]
    for cred in otp_creds:
        kc_admin.delete_credential(user_id=user_id, credential_id=cred["id"])
    
    return len(otp_creds)