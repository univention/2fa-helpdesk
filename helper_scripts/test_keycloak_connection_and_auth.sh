#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


: "${KEYCLOAK_ADMIN:?Need to set KEYCLOAK_ADMIN}"
: "${KEYCLOAK_PASSWORD:?Need to set KEYCLOAK_PASSWORD}"

# this is the way to get an OAuth-access token #
# the master-real admin will usually be fine for all realms #
TOKEN=$(curl -s -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$KEYCLOAK_ADMIN" \
  -d "password=$KEYCLOAK_PASSWORD" \
  -d 'grant_type=password' \
  -d 'client_id=admin-cli' \
  | jq -r .access_token)

echo $TOKEN

# List realm roles
curl -s -X GET "http://localhost:8080/admin/realms/opendesk/roles" \
  -H "Authorization: Bearer $TOKEN" | jq .
