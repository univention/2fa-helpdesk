# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH


from common import (user_is_redirected_to_password_login_form,
                    user_is_redirected_to_totp_setup, user_logs_in_with_password,
                    user_sets_up_totp)
from conftest import KeycloakUser
from playwright.sync_api import Page, expect

# The keycloak_users fixture creates its users under a dedicated mail domain,
# so searching for it matches exactly those and nothing else in the realm.
SHARED_USER_QUERY = "@multiple-users.com"
SHARED_USER_COUNT = 25

# Has to match the page size the frontend requests.
PAGE_SIZE = 10


def admin_opens_user_table(page: Page, url: str, admin: KeycloakUser):
    """Log in as a freshly created 2FA admin and wait for the user table."""
    page.goto(url)
    user_is_redirected_to_password_login_form(page)
    user_logs_in_with_password(page, admin)
    user_is_redirected_to_totp_setup(page)
    user_sets_up_totp(page, admin)
    page.wait_for_load_state("networkidle")
    expect(page.locator("table")).to_be_visible()


def type_search(page: Page, query: str):
    """Type a search term without waiting for anything to come back."""
    page.locator(".search-input").fill(query)


def search_for(page: Page, query: str):
    """Type a search term and wait for its results to arrive.

    Waiting matters: the field is debounced, and an unfiltered first page
    looks exactly like a filtered one from the outside (ten rows, another page
    available). Without waiting for the request the assertions below can pass
    against the pre-search list and the test then pages through the wrong set.
    """
    with page.expect_response(
        lambda response: "list_users" in response.url
        and response.request.method == "POST",
    ):
        type_search(page, query)


def test_admin_can_load_more_users(
        page: Page,
        admin_page_url: str,
        keycloak_2fa_admin: KeycloakUser,
        keycloak_users: list[KeycloakUser]):
    """Tests that "load more" appends a page at a time until the results run out."""
    admin_opens_user_table(page, admin_page_url, keycloak_2fa_admin)

    rows = page.locator("tbody tr")
    load_more = page.locator(".load-more-button")
    footer_hint = page.locator(".load-more-hint")

    search_for(page, SHARED_USER_QUERY)

    # First page only, with the button and its hint offering the way forward.
    expect(rows).to_have_count(PAGE_SIZE)
    expect(load_more).to_be_visible()
    expect(footer_hint).to_be_visible()

    # Each click appends a page instead of replacing the rows on screen.
    load_more.click()
    expect(rows).to_have_count(2 * PAGE_SIZE)

    load_more.click()
    expect(rows).to_have_count(SHARED_USER_COUNT)

    # Nothing left to fetch, so the button gives way to the end of list notice.
    expect(load_more).not_to_be_visible()
    expect(footer_hint).to_be_visible()


def test_load_more_keeps_previously_loaded_users(
        page: Page,
        admin_page_url: str,
        keycloak_2fa_admin: KeycloakUser,
        keycloak_users: list[KeycloakUser]):
    """Tests that loading a page appends to the list rather than replacing it."""
    admin_opens_user_table(page, admin_page_url, keycloak_2fa_admin)

    rows = page.locator("tbody tr")

    search_for(page, SHARED_USER_QUERY)
    expect(rows).to_have_count(PAGE_SIZE)

    first_page_usernames = [
        cell.inner_text() for cell in page.locator("tbody tr td:first-child").all()
    ]

    page.locator(".load-more-button").click()
    expect(rows).to_have_count(2 * PAGE_SIZE)

    usernames = [
        cell.inner_text() for cell in page.locator("tbody tr td:first-child").all()
    ]

    assert usernames[:PAGE_SIZE] == first_page_usernames, (
        "the first page was not kept on screen after loading the next one"
    )
    assert len(set(usernames)) == len(usernames), "the same user was listed twice"


def test_search_below_minimum_length_is_not_queried(
        page: Page,
        admin_page_url: str,
        keycloak_2fa_admin: KeycloakUser,
        keycloak_users: list[KeycloakUser]):
    """Tests that a search term under three characters is not sent to the backend."""
    admin_opens_user_table(page, admin_page_url, keycloak_2fa_admin)

    search_hint = page.locator(".search-hint")
    footer = page.locator(".table-footer")

    expect(search_hint).not_to_be_visible()

    # Two characters are too unspecific to be worth the lookup, so no request
    # is expected here and there is nothing to wait for.
    type_search(page, SHARED_USER_QUERY[:2])
    expect(search_hint).to_be_visible()

    # No request went out, so there is nothing to page through either.
    expect(footer).not_to_be_visible()

    # A third character makes the term searchable again.
    search_for(page, SHARED_USER_QUERY)
    expect(search_hint).not_to_be_visible()
    expect(page.locator("tbody tr")).to_have_count(PAGE_SIZE)
