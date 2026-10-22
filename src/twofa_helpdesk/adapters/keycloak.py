# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
import typing

import fastapi
import httpx
from pydantic import BaseModel


class User(BaseModel):
    keycloak_internal_id: str
    username: str
    email: typing.Optional[str] = None
    firstname: typing.Optional[str] = None
    lastname: typing.Optional[str] = None
    totp: typing.Optional[bool] = False


def _get_kc_admin() -> httpx.Client:
    """Return a client for the admin API of the configured realm, holding a fresh token"""

    try:
        server_url = os.environ["KEYCLOAK_URL"].rstrip("/")
        realm = os.environ["KEYCLOAK_REALM_NAME"]
        admin_realm = os.environ["KEYCLOAK_ADMIN_REALM_NAME"]
        credentials = {
            "grant_type": "password",
            "client_id": os.environ.get("KEYCLOAK_CLIENT_ID") or "admin-cli",
            "username": os.environ["KEYCLOAK_USERNAME"],
            "password": os.environ["KEYCLOAK_PASSWORD"],
        }
    except KeyError as e:
        raise fastapi.HTTPException(
            status_code=500,
            detail=f"Missing required Environment: {str(e)}",
        )

    verify = os.environ.get("KEYCLOAK_VERIFY_SSL", "true").lower() not in ("0", "false", "no")

    try:
        with httpx.Client(verify=verify) as client:
            response = client.post(
                f"{server_url}/realms/{admin_realm}/protocol/openid-connect/token",
                data=credentials,
            )
            response.raise_for_status()
            token = response.json()["access_token"]
    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500,
            detail=f"Keycloak connection error: {type(e)} - {str(e)}",
        )

    return httpx.Client(
        base_url=f"{server_url}/admin/realms/{realm}",
        headers={"Authorization": f"Bearer {token}"},
        verify=verify,
    )


def reset_2fa_token(user_id: str) -> int:
    """Reset the 2FA token for the give user"""

    with _get_kc_admin() as kc_admin:
        response = kc_admin.get(f"/users/{user_id}/credentials")
        response.raise_for_status()

        otp_creds = [i for i in response.json() if i["type"] == "otp"]
        for cred in otp_creds:
            kc_admin.delete(f"/users/{user_id}/credentials/{cred['id']}").raise_for_status()

    return len(otp_creds)


def list_users(query: str, page: int, limit: int) -> tuple[list[User], bool]:
    """List users based on a query (paginated)."""

    page -= 1

    query_struct = {
        "first": page * limit,
        "max": limit + 1,
    }

    if query:
        query_struct["search"] = f"*{query}*"  # For proper 'contains' search

    with _get_kc_admin() as kc_admin:
        response = kc_admin.get("/users", params=query_struct)
        response.raise_for_status()
        user_dicts = response.json()

    has_next = len(user_dicts) > limit
    user_dicts = user_dicts[:limit]

    users = [
        User(
            keycloak_internal_id=kc_user.get("id"),
            username=kc_user.get("username"),
            email=kc_user.get("email"),
            firstname=kc_user.get("firstName"),
            lastname=kc_user.get("lastName"),
            totp=kc_user.get("totp"),
        )
        for kc_user in user_dicts
    ]

    return users, has_next
