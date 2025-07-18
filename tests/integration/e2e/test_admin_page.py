# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


from common import (logout_user_from_browser, user_enters_otp_code,
                    user_is_redirected_to_otp_input_page,
                    user_is_redirected_to_password_login_form,
                    user_is_redirected_to_totp_setup,
                    user_logs_in_with_password, user_sets_up_totp)
from conftest import KeycloakUser
from playwright.sync_api import Page, expect


def test_2fa_admin_can_reset_user_2fa(
        page: Page,
        admin_page_url: str,
        self_service_url: str,
        keycloak_2fa_admin: KeycloakUser,
        keycloak_user: KeycloakUser):
    """Tests that an admin can reset a user's 2FA.
    """
    assert_user_must_setup_otp(page, self_service_url, keycloak_user)
    assert_user_must_login_with_otp(page, self_service_url, keycloak_user)
    assert_admin_can_reset_user_2fa(page, admin_page_url, keycloak_2fa_admin, keycloak_user)
    assert_user_must_setup_otp(page, self_service_url, keycloak_user)


def assert_user_must_setup_otp(page: Page, url: str, user: KeycloakUser):
    page.goto(url)
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)
    user_is_redirected_to_totp_setup(page)
    user_sets_up_totp(page, user)
    logout_user_from_browser(page, user)

def assert_user_must_login_with_otp(page: Page, url: str, user: KeycloakUser):
    page.goto(url)
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)

    user_is_redirected_to_otp_input_page(page)
    user_enters_otp_code(page, user)
    logout_user_from_browser(page, user)

def assert_admin_can_reset_user_2fa(
        page: Page,
        url: str,
        keycloak_2fa_admin: KeycloakUser,
        keycloak_user: KeycloakUser):
    page.goto(url)
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, keycloak_2fa_admin)
    user_is_redirected_to_totp_setup(page)
    user_sets_up_totp(page, keycloak_2fa_admin)
    page.wait_for_load_state("networkidle")

    btn = page.locator('tr', has_text=keycloak_user.username).locator('button')
    expect(btn).to_be_visible()
    btn.click()

    btn = page.locator('.modal-content').locator('button.primary')
    expect(btn).to_be_visible()
    btn.click()

    logout_user_from_browser(page, keycloak_2fa_admin)
