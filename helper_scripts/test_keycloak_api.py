#! /usr/bin/python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# This script tests authentication with a confidential client and deletion of a OTP Token from a user.
# How to use:
# 1) Create a Keycloak client with:
#   - Client Authentication: on
#   - Service Account Roles activated
#   - The SARs manage-users, query-users and view-users attached
# 2) Create a new user and configure and setup 2FA for them

HOSTNAME = "id.jahlers-opendesk.univention.dev"
REALM = "opendesk"
CLIENT_ID = "resttest"
CLIENT_SECRET = "sHYYBqgsVHr2mHDsG2PzhRYzesQqjLPr"
USERNAME = "test02"

# authenticate with the confidential client
r = requests.post(
    f"https://{HOSTNAME}/realms/{REALM}/protocol/openid-connect/token",
    verify=False,
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    },
)
access_token = r.json()["access_token"]

# search for the user to get the user id
r = requests.get(
    f"https://{HOSTNAME}/admin/realms/{REALM}/users",
    verify=False,
    headers={
        "Authorization": f"bearer {access_token}",
    },
    params={
        "username": USERNAME,
    },
)
user_id = r.json()[0]["id"]

# get the id of the users OTP credential object
r = requests.get(
    f"https://{HOSTNAME}/admin/realms/{REALM}/users/{user_id}/credentials",
    verify=False,
    headers={
        "Authorization": f"bearer {access_token}",
    },
)
otp_cred = [i for i in r.json() if i["type"] == "otp"]  # filter OTPs
if not otp_cred:
    print(f"ERROR: deletion of OTP from user {USERNAME} failed: user does not have a OTP set")
    exit(1)
cred_id = otp_cred[0]["id"]

# delete the OTP credential from the user object
r = requests.delete(
    f"https://{HOSTNAME}/admin/realms/{REALM}/users/{user_id}/credentials/{cred_id}",
    verify=False,
    headers={
        "Authorization": f"bearer {access_token}",
    },
)

if r.status_code == 204:
    print(f"Successfully deleted OTP from user {USERNAME}")
else:
    print(f"ERROR: deletion of OTP from user {USERNAME} failed")
    exit(1)
