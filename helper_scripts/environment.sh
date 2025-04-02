#!/bin/bash

if [ -z "$NAMESPACE" ]; then
    read -rp "Enter the namespace (or do export NAMESPACE= yourself): " NAMESPACE
fi

# get keycloak secrets
SECRET_NAME="ums-opendesk-keycloak-credentials"
SECRET_KEY="admin_password"

export KEYCLOAK_ADMIN=kcadmin
export KEYCLOAK_PASSWORD=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath="{.data.$SECRET_KEY}" \
                             | base64 -d)

# get UCS admin pw #
UCS_ADMIN_USER="Administrator"
UCS_ADMIN_PASS=$(kubectl -n "$NAMESPACE" get secrets ums-nubus-credentials -o jsonpath="{.data.administrator_password}" | base64 -d)

# TODO: is this the correct one?
# get guardian management API secret #
UCS_GUARDIAN_MGMT_SECRET=$(kubectl -n "$NAMESPACE" get secrets ums-opendesk-guardian-client-secret -o jsonpath="{.data.managementApiClientSecret}" | base64 -d)

# output all variables #
echo export NAMESPACE="$NAMESPACE"
echo export KEYCLOAK_ADMIN=$KEYCLOAK_ADMIN
echo export KEYCLOAK_PASSWORD="$KEYCLOAK_PASSWORD"
echo export UCS_ADMIN_USER="$UCS_ADMIN_USER"
echo export UCS_ADMIN_PASS="$UCS_ADMIN_PASS"
echo export UCS_GUARDIAN_MGMT_SECRET="$UCS_GUARDIAN_MGMT_SECRET"
