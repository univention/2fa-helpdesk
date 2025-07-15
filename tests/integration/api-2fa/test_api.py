# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import requests
from keycloak import KeycloakAdmin


def test_whoami(
    keycloak_user_with_totp,
    twofa_api_baseurl: str,
    session: requests.Session,
):
    access_token = keycloak_user_with_totp.get_access_token()

    resp = session.get(
        f"{twofa_api_baseurl}/whoami",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    assert resp_json["token"]["preferred_username"] == keycloak_user_with_totp.username
    assert not resp_json["twofa_admin"]


def test_reset_own_token(
    keycloak_user_with_totp,
    twofa_api_baseurl,
    session: requests.Session,
    keycloak_admin: KeycloakAdmin,
):
    credentials = keycloak_admin.get_credentials(keycloak_user_with_totp.id)

    assert any(credential["type"] == "otp" for credential in credentials), (
        "user does not have an OTP configured"
    )

    resp = session.post(
        f"{twofa_api_baseurl}/token/reset/own/",
        headers={
            "Authorization": f"Bearer {keycloak_user_with_totp.get_access_token()}",
        },
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    assert resp_json["resets_by_user"] == {keycloak_user_with_totp.id: 1}

    credentials = keycloak_admin.get_credentials(keycloak_user_with_totp.id or "")

    assert not any(credential["type"] == "otp" for credential in credentials), (
        "user still has an OTP token configured"
    )


def test_whoami_admin(
    keycloak_2fa_admin,
    twofa_api_baseurl: str,
    session: requests.Session,
):
    access_token = keycloak_2fa_admin.get_access_token()

    resp = session.get(
        f"{twofa_api_baseurl}/whoami",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    assert resp_json["token"]["preferred_username"] == keycloak_2fa_admin.username
    assert resp_json["twofa_admin"]


def test_reset_user_token_as_admin(
    keycloak_2fa_admin,
    keycloak_user_with_totp,
    twofa_api_baseurl,
    session: requests.Session,
    keycloak_admin: KeycloakAdmin,
):
    credentials = keycloak_admin.get_credentials(keycloak_user_with_totp.id)

    assert any(credential["type"] == "otp" for credential in credentials), (
        "user does not have an OTP configured"
    )

    request_body = {"user_ids": [keycloak_user_with_totp.id]}

    resp = session.post(
        f"{twofa_api_baseurl}/token/reset/user/",
        json=request_body,
        headers={"Authorization": f"Bearer {keycloak_2fa_admin.get_access_token()}"},
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    assert resp_json["resets_by_user"] == {keycloak_user_with_totp.id: 1}

    credentials = keycloak_admin.get_credentials(keycloak_user_with_totp.id)

    assert not any(credential["type"] == "otp" for credential in credentials), (
        "user still has an OTP token configured"
    )


def test_list_users_no_query(
    keycloak_2fa_admin,
    twofa_api_baseurl,
    session: requests.Session,
    keycloak_user_with_totp,
    known_keycloak_user_id,
):
    resp = session.post(
        f"{twofa_api_baseurl}/list_users",
        headers={"Authorization": f"Bearer {keycloak_2fa_admin.get_access_token()}"},
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    expected_users = {keycloak_2fa_admin.id, keycloak_user_with_totp.id}
    assert {
        user["keycloak_internal_id"] for user in resp_json["users"] \
            if user["keycloak_internal_id"] != known_keycloak_user_id
    } == expected_users


def test_list_users_with_query(
    keycloak_2fa_admin,
    twofa_api_baseurl,
    session: requests.Session,
    keycloak_user_with_totp,
):
    query = {"query": keycloak_2fa_admin.username}
    resp = session.post(
        f"{twofa_api_baseurl}/list_users",
        json=query,
        headers={"Authorization": f"Bearer {keycloak_2fa_admin.get_access_token()}"},
    )
    resp.raise_for_status()
    resp_json = resp.json()

    assert resp_json["success"]
    assert resp_json["total"] == 1
    expected_users = {keycloak_2fa_admin.id}
    assert {
        user["keycloak_internal_id"] for user in resp_json["users"]
    } == expected_users
