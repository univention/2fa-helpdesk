#!/usr/bin/python3

import os
import requests
import json

## Step 1: authenticate using Keycloak

# KEYCLOAK_ADMIN = os.environ["KEYCLOAK_ADMIN"]
# KEYCLOAK_PASSWORD = os.environ["KEYCLOAK_PASSWORD"]
#
# BASE_URL = "http://localhost:8080"
# REALM = "master"
# TARGET_REALM = "opendesk"
#
# token_url = f"{BASE_URL}/realms/{REALM}/protocol/openid-connect/token"
# token_data = {
#     "grant_type": "password",
#     "client_id": "admin-cli",
#     "username": KEYCLOAK_ADMIN,
#     "password": KEYCLOAK_PASSWORD,
# }
#
# token_headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/x-www-form-urlencoded",
# }
#
# token_resp = requests.post(token_url, data=token_data, headers=token_headers)
# token_resp.raise_for_status()
# access_token = token_resp.json()["access_token"]
#
# ## Step 2: test UDM Connection
# # TODO: This script totally does the wrong thing here, we're not testing the connection to UDM at all!
#
# query_url = f"{BASE_URL}/admin/realms/{TARGET_REALM}/users"
# query_params = {
#     "filter": "username=Administrator"
# }
# query_headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Accept": "application/json"
# }
#
# resp = requests.get(query_url, headers=query_headers, params=query_params)
# resp.raise_for_status()
#
# print(json.dumps(resp.json(), indent=2))

UCS_ADMIN = "Administrator"
UCS_ADMIN_PASS = "0ee416b7f0284b0bcc7f146e5e2407a5c8a36200"

BASE_URL = "localhost:9979"

#REALM = "master"
REALM = "opendesk"

r = requests.post(
    f"https://{BASE_URL}/realms/{REALM}/protocol/openid-connect/token",
    verify=False,
    data={
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": UCS_ADMIN,
        "password": UCS_ADMIN_PASS,
    }
)
print(r)
print(r.json())
access_token = r.json()["access_token"]
