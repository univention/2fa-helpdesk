# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import pytest

from twofa_helpdesk.adapters import keycloak

REALM = "test-realm"


@pytest.fixture
def keycloak_stub(httpserver, monkeypatch):
    """A Keycloak that answers the admin token request and nothing else."""
    httpserver.expect_request(
        "/realms/master/protocol/openid-connect/token",
        method="POST",
    ).respond_with_json({"access_token": "token", "expires_in": 60})
    monkeypatch.setenv("KEYCLOAK_URL", httpserver.url_for("/"))
    monkeypatch.setenv("KEYCLOAK_USERNAME", "admin")
    monkeypatch.setenv("KEYCLOAK_PASSWORD", "admin")
    monkeypatch.setenv("KEYCLOAK_REALM_NAME", REALM)
    monkeypatch.setenv("KEYCLOAK_ADMIN_REALM_NAME", "master")
    return httpserver


def test_list_users_trims_the_probe_row_and_reports_a_next_page(keycloak_stub):
    keycloak_stub.expect_request(f"/admin/realms/{REALM}/users").respond_with_json(
        [{"id": str(i), "username": f"user{i}"} for i in range(3)],
    )

    users, has_next = keycloak.list_users("", page=1, limit=2)

    assert [user.username for user in users] == ["user0", "user1"]
    assert has_next


def test_reset_2fa_token_deletes_only_otp_credentials(keycloak_stub):
    credentials = f"/admin/realms/{REALM}/users/user0/credentials"
    keycloak_stub.expect_request(credentials).respond_with_json(
        [{"id": "otp0", "type": "otp"}, {"id": "pw0", "type": "password"}],
    )
    keycloak_stub.expect_request(
        f"{credentials}/otp0",
        method="DELETE",
    ).respond_with_data("", status=204)

    assert keycloak.reset_2fa_token("user0") == 1
