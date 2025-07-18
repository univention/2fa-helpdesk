# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


from common import (logout_user_from_browser, user_enters_otp_code,
                    user_is_redirected_to_otp_input_page,
                    user_is_redirected_to_password_login_form,
                    user_is_redirected_to_totp_setup,
                    user_logs_in_with_password, user_sets_up_totp)
from conftest import KeycloakUser
from playwright.sync_api import Page, expect


def test_2fa_user_must_setup_totp_again_after_resetting_2fa(
        self_service_page: Page,
        keycloak_user: KeycloakUser):
    """Tests that a user can set up TOTP and reset 2FA."""
    assert_user_can_reset_2fa_via_self_service(self_service_page, keycloak_user)

def test_2fa_must_login_with_otp_after_totp_setup(
        self_service_page: Page,
        keycloak_user: KeycloakUser):
    """Tests that a user must log in with OTP after setting up TOTP."""
    assert_user_can_login_using_otp(self_service_page, keycloak_user)

def test_2fa_admin_must_setup_totp_again_after_resetting_2fa(
        self_service_page: Page,
        keycloak_2fa_admin: KeycloakUser):
    """Tests that an admin can set up TOTP and reset 2FA."""
    assert_user_can_reset_2fa_via_self_service(self_service_page, keycloak_2fa_admin)

def test_2fa_admin_must_login_with_otp_after_totp_setup(
        self_service_page: Page,
        keycloak_2fa_admin: KeycloakUser):
    """Tests that an admin must log in with OTP after setting up TOTP."""
    assert_user_can_login_using_otp(self_service_page, keycloak_2fa_admin)

def assert_user_can_reset_2fa_via_self_service(page: Page, user: KeycloakUser):
    """Helper function to assert that a user can reset 2FA via self-service."""
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)
    user_is_redirected_to_totp_setup(page)
    user_sets_up_totp(page, user)
    user_is_redirected_to_self_service(page)
    user_resets_own_2fa(page)
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)
    user_is_redirected_to_totp_setup(page)


def assert_user_can_login_using_otp(page: Page, user: KeycloakUser):
    """Helper function to assert that a user can log in using OTP after setting it up."""
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)
    user_is_redirected_to_totp_setup(page)
    user_sets_up_totp(page, user)
    logout_user_from_browser(page, user)

    page.reload()
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, user)

    user_is_redirected_to_otp_input_page(page)
    user_enters_otp_code(page, user)
    user_is_redirected_to_self_service(page)


def user_resets_own_2fa(page: Page):
    checkbox = page.locator("#confirm-reset")
    expect(checkbox).to_be_visible()
    checkbox.check()

    page.locator("button.primary:enabled").click()


def user_is_redirected_to_self_service(page: Page):
    # Wait for redirect to self-service page by checking for specific content
    page.wait_for_selector("text=Self Service")
