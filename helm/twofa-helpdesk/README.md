# twofa-helpdesk

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![AppVersion: 1.0.0](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)

2FA Helpdesk Backend API

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | ^0.18.x |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| extraIngresses | list | `[]` |  |
| global.affinity | object | `{}` |  |
| global.domain | string | `""` |  |
| global.environment | object | `{}` |  |
| global.fullnameOverride | string | `""` |  |
| global.host | string | `"twofa"` |  |
| global.imageRegistry | string | `"artifacts.software-univention.de"` |  |
| global.nameOverride | string | `""` |  |
| global.nodeSelector | object | `{}` |  |
| global.podAnnotations | object | `{}` |  |
| global.podSecurityContext | object | `{}` |  |
| global.postgresql.connection.host | string | `""` |  |
| global.postgresql.connection.port | string | `""` |  |
| global.replicaCount | int | `1` |  |
| global.restartPolicy | string | `"OnFailure"` |  |
| global.securityContext | object | `{}` |  |
| global.tolerations | list | `[]` |  |
| ingress.annotations | object | `{}` | Define custom ingress annotations for all Ingresses. |
| ingress.certManager.enabled | bool | `false` | Enable cert-manager.io annotaion. |
| ingress.certManager.issuerRef.kind | string | `"ClusterIssuer"` | Type of Issuer, f.e. "Issuer" or "ClusterIssuer". |
| ingress.certManager.issuerRef.name | string | `""` | Name of cert-manager.io Issuer resource. |
| ingress.enabled | bool | `true` | Enable creation of Ingress. |
| ingress.host | string | `""` | Define the Fully Qualified Domain Name (FQDN) where application should be reachable. (This will be the default for all Ingresses) |
| ingress.ingressClassName | string | `"nginx"` | The Ingress controlledebugr class name. (This will be the default for all Ingresses) |
| ingress.items[0].annotations | object | `{}` |  |
| ingress.items[0].host | string | `""` |  |
| ingress.items[0].ingressClassName | string | `""` |  |
| ingress.items[0].name | string | `"twofa-helpdesk-ui"` |  |
| ingress.items[0].paths | list | `[{"backend":{"service":{"name":"2fa-helpdesk-backend-ui","port":{"number":80},"suffix":"-ui"}},"path":"/ui","pathType":"Prefix"}]` | Define the Ingress paths. |
| ingress.items[0].tls.secretName | string | `""` |  |
| ingress.items[1].annotations | object | `{}` |  |
| ingress.items[1].host | string | `""` |  |
| ingress.items[1].ingressClassName | string | `""` |  |
| ingress.items[1].name | string | `"twofa-backend"` |  |
| ingress.items[1].paths[0].backend.service.name | string | `"2fa-helpdesk-backend"` |  |
| ingress.items[1].paths[0].backend.service.port.number | int | `8080` |  |
| ingress.items[1].paths[0].backend.service.suffix | string | `""` |  |
| ingress.items[1].paths[0].path | string | `"/backend"` |  |
| ingress.items[1].paths[0].pathType | string | `"Prefix"` |  |
| ingress.items[1].tls.secretName | string | `""` |  |
| ingress.tls | object | `{"enabled":true,"secretName":""}` | Secure an Ingress by specifying a Secret that contains a TLS private key and certificate.  Ref.: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls |
| ingress.tls.enabled | bool | `true` | Enable TLS/SSL/HTTPS for Ingress. |
| ingress.tls.secretName | string | `""` | The name of the kubernetes secret which contains a TLS private key and certificate. Hint: This secret is not created by this chart and must be provided. |
| keycloak | object | `{"admin_realm":"master","auth":{"existingSecret":{"keyMapping":{"adminPassword":null},"name":null},"password":"","username":"kcadmin"},"client":"twofa-helpdesk","connection":{"host":"","port":"8080"},"realm":""}` | Keycloak specific settings. |
| keycloak.auth.existingSecret | object | `{"keyMapping":{"adminPassword":null},"name":null}` | Keycloak password secret reference. |
| keycloak.auth.password | string | `""` | Keycloak password. |
| keycloak.auth.username | string | `"kcadmin"` | Keycloak user. |
| keycloak.client | string | `"twofa-helpdesk"` | Keycloak 2FA client name |
| keycloak.connection | object | `{"host":"","port":"8080"}` | Connection parameters. |
| keycloak.connection.host | string | `""` | Keycloak host. |
| keycloak.connection.port | string | `"8080"` | Keycloak port. |
| keycloak.realm | string | `""` | Keycloak realm. |
| provisioning.config.debug.enabled | bool | `true` |  |
| provisioning.containerSecurityContext.allowPrivilegeEscalation | bool | `false` |  |
| provisioning.containerSecurityContext.capabilities.drop[0] | string | `"ALL"` |  |
| provisioning.containerSecurityContext.enabled | bool | `true` |  |
| provisioning.containerSecurityContext.privileged | bool | `false` |  |
| provisioning.containerSecurityContext.readOnlyRootFilesystem | bool | `true` |  |
| provisioning.containerSecurityContext.runAsGroup | int | `1000` |  |
| provisioning.containerSecurityContext.runAsNonRoot | bool | `true` |  |
| provisioning.containerSecurityContext.runAsUser | int | `1000` |  |
| provisioning.containerSecurityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| provisioning.enabled | bool | `true` |  |
| provisioning.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| provisioning.image.pullSecrets | list | `[]` |  |
| provisioning.image.registry | string | `""` |  |
| provisioning.image.repository | string | `"nubus/images/wait-for-dependency"` |  |
| provisioning.image.sha256 | string | `""` |  |
| provisioning.image.tag | string | `"0.32.1@sha256:44d45067e1d4e7a00d3b651e56df5177087e3206368a45cd1816d78ba7b21347"` |  |
| provisioning.podSecurityContext.enabled | bool | `true` |  |
| provisioning.podSecurityContext.fsGroup | int | `1000` |  |
| provisioning.podSecurityContext.runAsGroup | int | `1000` |  |
| provisioning.podSecurityContext.runAsNonRoot | bool | `true` |  |
| provisioning.podSecurityContext.runAsUser | int | `1000` |  |
| provisioning.podSecurityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| provisioning.provisioningImage.imagePullPolicy | string | `"IfNotPresent"` |  |
| provisioning.provisioningImage.registry | string | `""` |  |
| provisioning.provisioningImage.repository | string | `"nubus/images/keycloak-bootstrap"` |  |
| provisioning.provisioningImage.sha256 | string | `""` |  |
| provisioning.provisioningImage.tag | string | `"0.12.1@sha256:4a36e3753bda7d6ccc6fc98f5e115bf96a4257c1a9458d075888256484cfdd4b"` |  |
| provisioning.tolerations | list | `[]` |  |
| twofaHelpdeskBackend.affinity | object | `{}` |  |
| twofaHelpdeskBackend.config.keycloak_url | string | `""` |  |
| twofaHelpdeskBackend.config.twofa_admin_groups[0] | string | `"/Domain Admins"` |  |
| twofaHelpdeskBackend.environment | object | `{}` |  |
| twofaHelpdeskBackend.fullnameOverride | string | `""` |  |
| twofaHelpdeskBackend.image.imagePullPolicy | string | `"Always"` |  |
| twofaHelpdeskBackend.image.imagePullSecrets | list | `[]` |  |
| twofaHelpdeskBackend.image.registry | string | `""` |  |
| twofaHelpdeskBackend.image.repository | string | `"nubus-dev/images/twofa-helpdesk-backend"` |  |
| twofaHelpdeskBackend.image.sha256 | string | `nil` | Define image sha256 as an alternative to `tag` |
| twofaHelpdeskBackend.image.tag | string | `"latest"` |  |
| twofaHelpdeskBackend.ingress.tls.secretName | string | `"twofa-backend-api-tls"` |  |
| twofaHelpdeskBackend.nameOverride | string | `""` |  |
| twofaHelpdeskBackend.nodeSelector | object | `{}` |  |
| twofaHelpdeskBackend.podAnnotations | object | `{}` |  |
| twofaHelpdeskBackend.podSecurityContext.enabled | bool | `true` |  |
| twofaHelpdeskBackend.podSecurityContext.fsGroup | int | `1000` |  |
| twofaHelpdeskBackend.podSecurityContext.fsGroupChangePolicy | string | `"Always"` | Change ownership and permission of the volume before being exposed inside a Pod. |
| twofaHelpdeskBackend.probes.liveness.enabled | bool | `true` |  |
| twofaHelpdeskBackend.probes.liveness.failureThreshold | int | `3` |  |
| twofaHelpdeskBackend.probes.liveness.initialDelaySeconds | int | `20` |  |
| twofaHelpdeskBackend.probes.liveness.periodSeconds | int | `30` |  |
| twofaHelpdeskBackend.probes.liveness.successThreshold | int | `1` |  |
| twofaHelpdeskBackend.probes.liveness.timeoutSeconds | int | `3` |  |
| twofaHelpdeskBackend.probes.readiness.enabled | bool | `true` |  |
| twofaHelpdeskBackend.probes.readiness.failureThreshold | int | `30` |  |
| twofaHelpdeskBackend.probes.readiness.initialDelaySeconds | int | `20` |  |
| twofaHelpdeskBackend.probes.readiness.periodSeconds | int | `15` |  |
| twofaHelpdeskBackend.probes.readiness.successThreshold | int | `1` |  |
| twofaHelpdeskBackend.probes.readiness.timeoutSeconds | int | `3` |  |
| twofaHelpdeskBackend.replicaCount | int | `1` |  |
| twofaHelpdeskBackend.resources | object | `{"limits":{"cpu":"4","memory":"4Gi"},"requests":{"cpu":"250m","memory":"512Mi"}}` | Deployment resources for the listener container |
| twofaHelpdeskBackend.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| twofaHelpdeskBackend.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| twofaHelpdeskBackend.securityContext.enabled | bool | `true` |  |
| twofaHelpdeskBackend.securityContext.privileged | bool | `false` |  |
| twofaHelpdeskBackend.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| twofaHelpdeskBackend.securityContext.runAsGroup | int | `1000` |  |
| twofaHelpdeskBackend.securityContext.runAsNonRoot | bool | `true` |  |
| twofaHelpdeskBackend.securityContext.runAsUser | int | `1000` |  |
| twofaHelpdeskBackend.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| twofaHelpdeskBackend.service.enabled | bool | `true` |  |
| twofaHelpdeskBackend.service.ports.http.containerPort | int | `8080` |  |
| twofaHelpdeskBackend.service.ports.http.port | int | `8080` |  |
| twofaHelpdeskBackend.service.ports.http.protocol | string | `"TCP"` |  |
| twofaHelpdeskBackend.service.sessionAffinity.enabled | bool | `false` |  |
| twofaHelpdeskBackend.service.sessionAffinity.timeoutSeconds | int | `10800` |  |
| twofaHelpdeskBackend.service.type | string | `"ClusterIP"` |  |
| twofaHelpdeskBackend.tolerations | list | `[]` |  |
| twofaHelpdeskFrontend.affinity | object | `{}` |  |
| twofaHelpdeskFrontend.environment | object | `{}` |  |
| twofaHelpdeskFrontend.fullnameOverride | string | `""` |  |
| twofaHelpdeskFrontend.image.imagePullPolicy | string | `"Always"` |  |
| twofaHelpdeskFrontend.image.imagePullSecrets | list | `[]` |  |
| twofaHelpdeskFrontend.image.registry | string | `""` |  |
| twofaHelpdeskFrontend.image.repository | string | `"nubus-dev/images/twofa-helpdesk-frontend"` |  |
| twofaHelpdeskFrontend.image.sha256 | string | `nil` | Define image sha256 as an alternative to `tag` |
| twofaHelpdeskFrontend.image.tag | string | `"latest"` |  |
| twofaHelpdeskFrontend.nameOverride | string | `""` |  |
| twofaHelpdeskFrontend.nginx.disableIPv6 | bool | `true` |  |
| twofaHelpdeskFrontend.nodeSelector | object | `{}` |  |
| twofaHelpdeskFrontend.podAnnotations | object | `{}` |  |
| twofaHelpdeskFrontend.podSecurityContext.enabled | bool | `true` |  |
| twofaHelpdeskFrontend.podSecurityContext.fsGroup | int | `1000` |  |
| twofaHelpdeskFrontend.podSecurityContext.fsGroupChangePolicy | string | `"Always"` | Change ownership and permission of the volume before being exposed inside a Pod. |
| twofaHelpdeskFrontend.podSecurityContext.sysctls[0].name | string | `"net.ipv4.ip_unprivileged_port_start"` |  |
| twofaHelpdeskFrontend.podSecurityContext.sysctls[0].value | string | `"1"` |  |
| twofaHelpdeskFrontend.probes.liveness.enabled | bool | `true` |  |
| twofaHelpdeskFrontend.probes.liveness.failureThreshold | int | `3` |  |
| twofaHelpdeskFrontend.probes.liveness.initialDelaySeconds | int | `20` |  |
| twofaHelpdeskFrontend.probes.liveness.periodSeconds | int | `30` |  |
| twofaHelpdeskFrontend.probes.liveness.successThreshold | int | `1` |  |
| twofaHelpdeskFrontend.probes.liveness.timeoutSeconds | int | `3` |  |
| twofaHelpdeskFrontend.probes.readiness.enabled | bool | `true` |  |
| twofaHelpdeskFrontend.probes.readiness.failureThreshold | int | `30` |  |
| twofaHelpdeskFrontend.probes.readiness.initialDelaySeconds | int | `20` |  |
| twofaHelpdeskFrontend.probes.readiness.periodSeconds | int | `15` |  |
| twofaHelpdeskFrontend.probes.readiness.successThreshold | int | `1` |  |
| twofaHelpdeskFrontend.probes.readiness.timeoutSeconds | int | `3` |  |
| twofaHelpdeskFrontend.replicaCount | int | `1` |  |
| twofaHelpdeskFrontend.resources | object | `{"limits":{"cpu":"4","memory":"4Gi"},"requests":{"cpu":"250m","memory":"512Mi"}}` | Deployment resources for the listener container |
| twofaHelpdeskFrontend.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| twofaHelpdeskFrontend.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| twofaHelpdeskFrontend.securityContext.enabled | bool | `true` |  |
| twofaHelpdeskFrontend.securityContext.privileged | bool | `false` |  |
| twofaHelpdeskFrontend.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| twofaHelpdeskFrontend.securityContext.runAsGroup | int | `1000` |  |
| twofaHelpdeskFrontend.securityContext.runAsNonRoot | bool | `true` |  |
| twofaHelpdeskFrontend.securityContext.runAsUser | int | `1000` |  |
| twofaHelpdeskFrontend.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| twofaHelpdeskFrontend.service.enabled | bool | `true` |  |
| twofaHelpdeskFrontend.service.ports.http.containerPort | int | `80` |  |
| twofaHelpdeskFrontend.service.ports.http.port | int | `80` |  |
| twofaHelpdeskFrontend.service.ports.http.protocol | string | `"TCP"` |  |
| twofaHelpdeskFrontend.service.sessionAffinity.enabled | bool | `false` |  |
| twofaHelpdeskFrontend.service.sessionAffinity.timeoutSeconds | int | `10800` |  |
| twofaHelpdeskFrontend.service.type | string | `"ClusterIP"` |  |
| twofaHelpdeskFrontend.tolerations | list | `[]` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.3](https://github.com/norwoodj/helm-docs/releases/v1.11.3)
