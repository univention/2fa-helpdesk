# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from time import sleep, time

import pyotp
from conftest import KeycloakUser
from playwright.sync_api import Page, expect


def user_is_redirected_to_password_login_form(page: Page):
    expect(page.locator('input[name="username"]')).to_be_visible()
    expect(page.locator('input[name="password"]')).to_be_visible()
    expect(page.locator('button[type="submit"]')).to_be_visible()


def user_logs_in_with_password(page: Page, keycloak_user: KeycloakUser):
    page.fill('input[name="username"]', keycloak_user.username)
    page.fill('input[name="password"]', keycloak_user.password)
    page.click('button[type="submit"]')


def user_is_redirected_to_totp_setup(page: Page):
    page.wait_for_load_state("networkidle")
    page.wait_for_selector('text="Unable to scan?"', timeout=5000)


def user_is_redirected_to_otp_input_page(page: Page):
    """Wait for the OTP input page where user needs to enter one-time code."""
    page.wait_for_load_state("networkidle")
    page.wait_for_selector('input[name="otp"]', timeout=5000)
    page.wait_for_selector('text="One-time code"', timeout=5000)


def user_enters_otp_code(page: Page, keycloak_user: KeycloakUser):
    """Enter the current OTP code for the user."""
    if not keycloak_user.totp:
        raise ValueError("User does not have TOTP configured")

    max_attempts = 3
    for attempt in range(max_attempts):
        if attempt > 0:
            sleep(1)

        future_timestamp = int(time()) + keycloak_user.totp.interval
        current_otp = keycloak_user.totp.at(future_timestamp)

        page.fill('input[name="otp"]', "")
        page.fill('input[name="otp"]', str(current_otp))
        page.click('button[name="login"]')

        try:
            page.wait_for_load_state("networkidle", timeout=5000)
            otp_input = page.locator('input[name="otp"]')
            if not otp_input.is_visible():
                return
        except Exception:
            continue

    raise ValueError(f"Failed to enter correct OTP code after {max_attempts} attempts")


def user_sets_up_totp(page: Page, keycloak_user: KeycloakUser):
    page.click('text="Unable to scan?"')
    page.wait_for_selector('#kc-totp-secret-key', timeout=5000)
    totp_secret = page.locator('#kc-totp-secret-key').text_content()

    clean_secret = totp_secret.replace(" ", "").strip()
    totp = pyotp.TOTP(clean_secret)

    # Store the TOTP secret in the KeycloakUser instance for later use
    keycloak_user.set_totp(clean_secret)

    page.fill('input[name="totp"]', totp.now())
    page.fill('input[name="userLabel"]', "Test Device")
    page.click('input[type="submit"]')


def logout_user_from_browser(page: Page, keycloak_user: KeycloakUser):
    """Logout user by clearing browser session and calling Keycloak logout."""
    try:
        keycloak_user.logout()
    except Exception as e:
        print(f"Keycloak logout failed: {e}")

    page.context.clear_cookies()
    page.context.clear_permissions()

    try:
        page.evaluate("window.localStorage.clear();")
        page.evaluate("window.sessionStorage.clear();")
    except Exception:
        pass
