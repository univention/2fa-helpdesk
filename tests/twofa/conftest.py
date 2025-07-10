# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
import requests
from bs4 import BeautifulSoup, Tag
from keycloak import KeycloakAdmin, KeycloakOpenID
import pyotp
from faker import Faker
from dataclasses import dataclass
import os


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
    }

    resp = session.post(totp_submit_form_action, data=data)
    resp.raise_for_status()

    credentials = keycloak_admin.get_credentials(keycloak_user.id)
    assert any(credential["type"] == "otp" for credential in credentials)

    keycloak_user.set_totp(totp_secret)

    return keycloak_user
