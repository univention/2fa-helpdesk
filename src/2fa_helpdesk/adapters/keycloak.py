# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
import keycloak
import fastapi
import typing
from pydantic import BaseModel
class User(BaseModel):

    keycloak_internal_id: str
    username: str
    email: typing.Optional[str] = None
    firstname: typing.Optional[str] = None
    lastname: typing.Optional[str] = None
    totp: typing.Optional[bool] = False

def _get_kc_admin():
    try:
        kc_admin = keycloak.KeycloakAdmin(
            server_url=os.environ["KEYCLOAK_URL"],
            username=os.environ["KEYCLOAK_USERNAME"],
            password=os.environ["KEYCLOAK_PASSWORD"],
            realm_name=os.environ["KEYCLOAK_REALM_NAME"],
            user_realm_name=os.environ["KEYCLOAK_ADMIN_REALM_NAME"],
            client_id=os.environ.get("KEYCLOAK_CLIENT_ID") or "admin-cli",
            verify=os.environ.get("KEYCLOAK_VERIFY_SSL") or True,
        )
        return kc_admin
    except KeyError as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Missing required Environment: {str(e)}",
        )
    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Keycloak connection error: {type(e)} - {str(e)}",
        )


def reset_2fa_token(user_id: str) -> dict:
    '''Reset the 2FA token for the give user'''

    kc_admin = _get_kc_admin()

    credentials = kc_admin.get_credentials(user_id=user_id)

    otp_creds = [i for i in credentials if i["type"] == "otp"]
    for cred in otp_creds:
        kc_admin.delete_credential(user_id=user_id, credential_id=cred["id"])

    return len(otp_creds)

def list_users(query: str, page: int, limit: int) -> typing.Tuple[list[User], int]:
    '''List users based on a query (paginated)'''

    # FIXME: frontend current 1-indexes pages, is that correct?
    page -= 1

    kc_admin = _get_kc_admin()

    # generate paginated query #
    query_struct_with_pages = {
        "search" : query or "*@*",
        "first": page*limit,
        "max": limit,
    }

    # generate user count query #
    query_struct_user_count = {
        "search" : query or "*@*",
        "briefRepresentation": True,
    }

    user_dicts = kc_admin.get_users(query=query_struct_with_pages)

    # FIXME broken on keycloak-side
    # total_for_this_query = kc_admin.users_count(query=query_struct)
    total_for_this_query = len(kc_admin.get_users(query_struct_user_count))

    # generate fastapi objects from users #
    users = []
    for kc_user in user_dicts:

        users.append(
            User(
                keycloak_internal_id=kc_user.get("id"),
                username=kc_user.get('username'),
                email=kc_user.get('email'),
                firstname=kc_user.get('firstName'),
                lastname=kc_user.get('lastName'),
                totp=kc_user.get('totp'),
            ),
        )

    return users, total_for_this_query
