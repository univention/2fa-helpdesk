#!/bin/bash
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

set -e

BACKEND_PORT="8188"

kubectl get configmap nubus-helpdesk-ui -o jsonpath='{.data.config\.json}' \
  | jq --arg api_url "http://localhost:${BACKEND_PORT}/backend" '.VITE_API_URL = $api_url' \
  > "config.json"
VITE_KEYCLOAK_URL="$(jq -r .VITE_KEYCLOAK_URL config.json)"

# backend also needs to be run locally because of CORS rules
OIDC_REALM="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.OIDC_REALM}')"
OIDC_CLIENT_ID="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.OIDC_CLIENT_ID}')"
KEYCLOAK_USERNAME="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.KEYCLOAK_USERNAME}')"
KEYCLOAK_PASSWORD="$(kubectl get secret nubus-keycloak-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)"
KEYCLOAK_REALM_NAME="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.KEYCLOAK_REALM_NAME}')"
KEYCLOAK_CLIENT_ID="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.KEYCLOAK_CLIENT_ID}')"
KEYCLOAK_ADMIN_REALM_NAME="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.KEYCLOAK_ADMIN_REALM_NAME}')"
TWOFA_ADMIN_GROUPS="$(kubectl get configmap nubus-helpdesk-config -o jsonpath='{.data.TWOFA_ADMIN_GROUPS}')"

function cleanup {
  docker stop "${container_id}"
  rm "config.json"
}
trap cleanup EXIT

docker_name="univention/2fa-helpdesk-backend"
docker build -q -f "../docker/twofa-helpdesk-backend/Dockerfile" --tag "${docker_name}" ../
container_id=$( \
  docker run \
    -e "OIDC_HOST=${VITE_KEYCLOAK_URL}" \
    -e "OIDC_REALM=${OIDC_REALM}" \
    -e "OIDC_CLIENT_ID=${OIDC_CLIENT_ID}" \
    -e "KEYCLOAK_URL=${VITE_KEYCLOAK_URL}" \
    -e "KEYCLOAK_USERNAME=${KEYCLOAK_USERNAME}" \
    -e "KEYCLOAK_PASSWORD=${KEYCLOAK_PASSWORD}" \
    -e "KEYCLOAK_REALM_NAME=${KEYCLOAK_REALM_NAME}" \
    -e "KEYCLOAK_CLIENT_ID=${KEYCLOAK_CLIENT_ID}" \
    -e "KEYCLOAK_ADMIN_REALM_NAME=${KEYCLOAK_ADMIN_REALM_NAME}" \
    -e "TWOFA_ADMIN_GROUPS=${TWOFA_ADMIN_GROUPS}" \
    -e "PREFIX=/backend" \
    -e "CORS_ALLOW=http://localhost:5173" \
    -p "127.0.0.1:${BACKEND_PORT}:8080" \
    -d \
    "${docker_name}"
)
echo "Backend docker container started: ${container_id}"

echo ""
echo "---------------------------"
echo "Please make sure your nubus keycloak is configured correctly to allow localhost":
echo "  * add http://localhost:5173/ to the Web origins in the twofa-helpdesk client"
echo "  * add http://localhost:5173/* to the Valid redirect URIs in the twofa-helpdesk client"
echo "  * add http://localhost:5173/ to the CSP in the Realm settings -> security defenses tab"
echo "---------------------------"
echo ""

yarn run dev --clearScreen false
