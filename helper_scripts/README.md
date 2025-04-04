# Dev- & Helper-Scrpts

The intention of these helper scripts is to expose and test, relevant APIs locally and give examples on how to authenticate correctly and retrieve the correct secrets from an existing nubus/opendesk deployment.

# How to use
Run `./environment.sh` to retrieve secrets and set environment variables, run without backticks to see the output:

    `./environment.sh`

Alternatively, use [direnv](https://direnv.net/) to manage your environment variables, example `.envrc`:

```bash
export KUBECONFIG="$HOME/.kube/gaia.yaml"
export NAMESPACE="uv-jahlers-opendesk"
export DOMAIN="jahlers-opendesk.univention.dev"
kubectl config set-context --current --namespace=$NAMESPACE

# get keycloak secrets
SECRET_NAME="ums-opendesk-keycloak-credentials"
SECRET_KEY="admin_password"

export KEYCLOAK_ADMIN=kcadmin
export KEYCLOAK_PASSWORD=$(kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" -o jsonpath="{.data.$SECRET_KEY}" \
                             | base64 -d)

# get UCS admin pw #
export UCS_ADMIN_USER="Administrator"
export UCS_ADMIN_PASS=$(kubectl -n "$NAMESPACE" get secrets ums-nubus-credentials -o jsonpath="{.data.administrator_password}" | base64 -d)

# TODO: is this the correct one?
# get guardian management API secret #
export UCS_GUARDIAN_MGMT_SECRET=$(kubectl -n "$NAMESPACE" get secrets ums-opendesk-guardian-client-secret -o jsonpath="{.data.managementApiClientSecret}" | base64 -d)
```

then run `forward_ports.sh` in a different window:

    ./forward_ports.sh

if you need more forwards in the future, just extend the relevant section here:

    port_forwards=(
      "pod/ums-keycloak-0 8080:8080 8443:8443"
      "pod/${UDM_CONTAINER} 9979:9979"
    )

Then run the connection scripts to test connectivity and authentication:

    ./test_keycloak_connection_and_auth.sh
    ./test_udm_connection.py

Both should output some JSON, keycloak roles and UDM user matching *"Administrator"* to be exact.

# Guardian
There is a guardian management API secret but not sure what it does. In general I don't understand how I'm supposed to use it, so maybe one of you could find out more.

# Keycloak
We can test if the client for the Keycloak Rest API is correctly set up for our use case (see comments in the script on how to set this up):

    ./test_keycloak_api.py

# Finding out new ports
To find ports of pods in case you need it for forward, use this commands to find the pod if it has a weird name and then get the ports (example for guardian):

    export NAMESPACE=yschmidt-opendesk
    export POD_PREFIX=ums-guardian-authorization-api-
    export POD=$(kubectl get pods -n $NAMESPACE --no-headers | grep $POD_PREFIX | head -n 1 | awk '{print $1}')
    kubectl get pod -n yschmidt-opendesk ${POD} -o jsonpath='{.spec.containers[*].ports}' | jq .
