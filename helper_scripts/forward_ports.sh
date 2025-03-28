#!/bin/bash

if [ -z "$NAMESPACE" ]; then
    echo "Set \$NAMESPACE before running please."
    exit 1
fi

NAMESPACE="yschmidt-opendesk"

UDM_CONTAINER=$(kubectl get pods -n yschmidt-opendesk --no-headers | grep '^ums-udm-rest-api-' | head -n 1 | awk '{print $1}')
port_forwards=(
  "pod/ums-keycloak-0 8080:8080 8443:8443"
  "pod/${UDM_CONTAINER} 9979:9979"
)

pids=()

for pf in "${port_forwards[@]}"; do
  echo "Starting port-forward: $pf"
  kubectl port-forward -n "$NAMESPACE" $pf >/dev/null 2>&1 &
  pids+=($!)
done

cleanup() {
  echo "Stopping all port-forwards..."
  for pid in "${pids[@]}"; do
    kill "$pid" 2>/dev/null
  done
}
trap cleanup EXIT

echo "All port-forwards started."
read -p "Press Enter to stop..."
