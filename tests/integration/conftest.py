# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import json
import os
from dataclasses import dataclass

import pyotp
import pytest
import requests
from bs4 import BeautifulSoup, Tag
from faker import Faker
from keycloak import KeycloakAdmin, KeycloakOpenID
from playwright.sync_api import Page


@dataclass
class KeycloakUser:
    """Represents a Keycloak user with TOTP authentication."""

    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    server_url: str
    realm: str
    client_id: str
    id: str
    totp: pyotp.TOTP | None = None

    def set_totp(self, secret: str):
        self.totp = pyotp.TOTP(secret)

    def generate_otp(self) -> int | None:
        """Generate current TOTP code."""
        if not self.totp:
            return None

        return int(self.totp.now())

    def get_tokens(self) -> dict:
        """Get tokens using Resource Owner Password Credentials flow with OTP."""
        keycloak_openid = KeycloakOpenID(
            server_url=self.server_url,
            client_id=self.client_id,
            realm_name=self.realm,
        )
        token = keycloak_openid.token(username=self.username, password=self.password)
        return token

    def get_access_token(self):
        """Return the access token for this user"""
        tokens = self.get_tokens()
        return tokens["access_token"]

    def logout(self):
        """Logout user by calling Keycloak logout endpoint."""
        keycloak_openid = KeycloakOpenID(
            server_url=self.server_url,
            client_id=self.client_id,
            realm_name=self.realm,
        )
        try:
            tokens = self.get_tokens()
            refresh_token = tokens.get("refresh_token")

            if refresh_token:
                keycloak_openid.logout(refresh_token)
        except Exception as e:
            print(f"Logout failed (this may be expected): {e}")

    def to_keycloak_payload(self) -> dict:
        """Convert to Keycloak user creation payload."""
        return {
            "email": self.email,
            "emailVerified": True,
            "enabled": True,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "username": self.username,
            "credentials": [
                {"type": "password", "value": self.password, "temporary": False},
            ],
            "groups": ["2fa-users"],
        }


def get_input_value(soup: BeautifulSoup, name: str) -> str:
    """Get value from input field by name."""
    input_tag = soup.find("input", {"name": name})
    assert isinstance(input_tag, Tag)
    input_value = input_tag.get("value")
    assert isinstance(input_value, str)
    return input_value


def get_contents(soup: BeautifulSoup, element: str, id: str) -> str:
    """Get contents of an HTML element by tag and id."""
    html_tag = soup.find(element, {"id": id})
    assert isinstance(html_tag, Tag)
    return html_tag.decode_contents()


@pytest.fixture()
def twofa_api_baseurl():
    """2FA API base URL from environment variable."""
    return os.getenv("TWOFA_API_BASEURL", "http://localhost:8081")


@pytest.fixture
def keycloak_server_url():
    """Keycloak server URL from environment variable."""
    return os.getenv("KEYCLOAK_URL", "http://localhost:8080")


@pytest.fixture
def keycloak_admin_username():
    """Keycloak admin username from environment variable."""
    return os.getenv("KEYCLOAK_USERNAME", "admin")


@pytest.fixture
def keycloak_admin_password():
    """Keycloak admin password from environment variable."""
    return os.getenv("KEYCLOAK_PASSWORD", "admin")


@pytest.fixture
def keycloak_realm_name():
    """Keycloak realm name from environment variable."""
    return os.getenv("KEYCLOAK_REALM_NAME", "test-realm")


@pytest.fixture
def keycloak_user_realm_name():
    """Keycloak user realm name from environment variable."""
    return os.getenv("KEYCLOAK_ADMIN_REALM_NAME", "master")


@pytest.fixture
def keycloak_client_id():
    """Keycloak client ID from environment variable."""
    return os.getenv("OIDC_CLIENT_ID", "2fa-helpdesk")


@pytest.fixture
def keycloak_admin(
    keycloak_server_url,
    keycloak_admin_username,
    keycloak_admin_password,
    keycloak_realm_name,
    keycloak_user_realm_name,
):
    """Keycloak admin client."""
    return KeycloakAdmin(
        server_url=keycloak_server_url,
        username=keycloak_admin_username,
        password=keycloak_admin_password,
        realm_name=keycloak_realm_name,
        user_realm_name=keycloak_user_realm_name,
    )


@pytest.fixture
def fake():
    """Faker instance for generating test data."""
    return Faker()


def _create_kc_user(
    groups: list[str],
    keycloak_server_url,
    keycloak_realm_name,
    keycloak_client_id,
    keycloak_admin: KeycloakAdmin,
    fake,
) -> KeycloakUser:
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = fake.user_name()
    password = fake.password()
    email = f"{username}@example.com"

    kc_payload = {
        "email": email,
        "emailVerified": True,
        "enabled": True,
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "credentials": [{"type": "password", "value": password, "temporary": False}],
        "groups": groups,
    }

    resp = keycloak_admin.create_user(kc_payload)

    user = KeycloakUser(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        server_url=keycloak_server_url,
        realm=keycloak_realm_name,
        client_id=keycloak_client_id,
        id=resp,
    )

    return user


@pytest.fixture
def keycloak_2fa_admin(
    fake,
    keycloak_admin,
    keycloak_server_url,
    keycloak_realm_name,
    keycloak_client_id,
):
    user = _create_kc_user(
        ["2FA Admins"],
        keycloak_server_url,
        keycloak_realm_name,
        keycloak_client_id,
        keycloak_admin,
        fake,
    )

    yield user

    try:
        keycloak_admin.delete_user(user.id)
    except Exception as e:
        print(f"Failed to delete created keycloak user: {e}")


@pytest.fixture
def keycloak_user(
    fake,
    keycloak_admin,
    keycloak_server_url,
    keycloak_realm_name,
    keycloak_client_id,
):
    user = _create_kc_user(
        ["2fa-users"],
        keycloak_server_url,
        keycloak_realm_name,
        keycloak_client_id,
        keycloak_admin,
        fake,
    )

    yield user

    try:
        keycloak_admin.delete_user(user.id)
    except Exception as e:
        print(f"Failed to delete created keycloak user: {e}")


@pytest.fixture
def session():
    """Requests session for HTTP operations."""
    return requests.Session()


BS_HTML_PARSER = "html.parser"


def extract_kc_login_form_action(soup: BeautifulSoup) -> str:
    login_form = soup.find("form", {"id": "kc-form-login"})
    assert login_form, "login form not found"
    assert isinstance(login_form, Tag), "login form is not a Tag"
    form_action = login_form.get("action")
    assert form_action
    assert isinstance(form_action, str)

    return form_action


def extract_kc_totp_manual_setup_url(soup: BeautifulSoup) -> str:
    manual_setup_tag = soup.find("a", {"id": "mode-manual"})
    assert isinstance(manual_setup_tag, Tag)
    manual_setup_url = manual_setup_tag.get("href")
    assert isinstance(manual_setup_url, str)

    return manual_setup_url


@pytest.fixture
def keycloak_user_with_totp(
    keycloak_user: KeycloakUser,
    session: requests.Session,
    keycloak_admin: KeycloakAdmin,
):
    """Configure TOTP for an existing Keycloak user."""
    # Set up TOTP for the user
    uri_parameters = {
        "response_type": "code",
        "client_id": keycloak_user.client_id,
        "kc_action": "CONFIGURE_TOTP",
    }
    login_dialog = session.get(
        f"{keycloak_user.server_url}/realms/{keycloak_user.realm}/protocol/openid-connect/auth",
        params=uri_parameters,
    )
    soup = BeautifulSoup(login_dialog.text, BS_HTML_PARSER)
    form_action = extract_kc_login_form_action(soup)

    # needed to send "secure" cookies to Keycloak without using HTTPS
    for cookie in session.cookies:
        cookie.secure = False

    login_response = session.post(
        form_action,
        data={"username": keycloak_user.username, "password": keycloak_user.password},
    )
    soup = BeautifulSoup(login_response.text, BS_HTML_PARSER)

    manual_setup_url = extract_kc_totp_manual_setup_url(soup)

    totp_manual_response = session.get(manual_setup_url)
    soup = BeautifulSoup(totp_manual_response.text, BS_HTML_PARSER)

    totp_secret = get_contents(soup, "span", "kc-totp-secret-key").replace(" ", "")

    totp_submit_form_tag = soup.find("form", {"id": "kc-totp-settings-form"})
    assert isinstance(totp_submit_form_tag, Tag)

    totp_submit_form_action = totp_submit_form_tag.get("action")
    assert isinstance(totp_submit_form_action, str)

    totp = pyotp.TOTP(totp_secret)
    data = {
        "userLabel": "foo",
        "totp": totp.now(),
        "totpSecret": get_input_value(soup, "totpSecret"),
        "mode": "manual",
        "logout-sessions": "on",
    }

    resp = session.post(totp_submit_form_action, data=data, allow_redirects=False)
    resp.raise_for_status()

    credentials = keycloak_admin.get_credentials(keycloak_user.id)
    assert any(credential["type"] == "otp" for credential in credentials)

    keycloak_user.set_totp(totp_secret)

    return keycloak_user

@pytest.fixture
def known_keycloak_user_id():
    """Find the user 'test' in the realm export file and return their ID."""
    realm_file_path = "tests/integration/data/export/realm-export-with-user.json"

    with open(realm_file_path, 'r') as f:
        realms = json.load(f)

    # Look through all realms for the user 'test'
    for realm in realms:
        if 'users' in realm:
            for user in realm['users']:
                if user.get("username") == "test":
                    return user["id"]

    raise ValueError("User 'test' not found in realm export file")

@pytest.fixture
def frontend_base_url():
    """Fixture to provide the frontend base URL."""
    return os.getenv("FRONTEND_URL", "http://localhost:3000")

@pytest.fixture
def self_service_url(frontend_base_url: str):
    """Fixture to provide the self-service URL."""
    return f"{frontend_base_url}/univention/2fa/self-service"

@pytest.fixture
def admin_page_url(frontend_base_url: str):
    """Fixture to provide the admin page URL."""
    return f"{frontend_base_url}/univention/2fa/admin"


@pytest.fixture
def self_service_page(page: Page, self_service_url: str):
    """Fixture to provide the self-service."""
    page.goto(self_service_url)
    return page

@pytest.fixture
def admin_page(page: Page, admin_page_url: str):
    """Fixture to provide the admin page."""
    page.goto(admin_page_url)
    return page
