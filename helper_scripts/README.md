# Dev- & Helper-Scrpts

The intention of these helper scripts is to expose and test, relevant APIs locally and give examples on how to authenticate correctly and retrieve the correct secrets from an existing nubus/opendesk deployment.

# How to use
Run `./environment.sh` to retrieve secrets and set environment variables, run without backticks to see the output:

    `./environment.sh`

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

# Finding out new ports
To find ports of pods in case you need it for forward, use this commands to find the pod if it has a weird name and then get the ports (example for guardian):

    export NAMESPACE=yschmidt-opendesk
    export POD_PREFIX=ums-guardian-authorization-api-
    export POD=$(kubectl get pods -n $NAMESPACE --no-headers | grep $POD_PREFIX | head -n 1 | awk '{print $1}')
    kubectl get pod -n yschmidt-opendesk ${POD} -o jsonpath='{.spec.containers[*].ports}' | jq .
