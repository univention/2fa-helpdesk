# twofa-helpdesk

2FA Helpdesk Backend API

- **Version**: 0.1.0
- **Type**:
- **AppVersion**: 1.0.0
-

## TL;DR

```console
helm upgrade --install twofa-helpdesk oci://artifacts.software-univention.de/nubus-dev/charts/twofa-helpdesk
```

## Introduction

This chart does install the 2FA-Helpdesk.

## Installing

To install the chart with the release name `twofa-helpdesk`:

```console
helm upgrade --install twofa-helpdesk oci://artifacts.software-univention.de/nubus-dev/charts/twofa-helpdesk
```

## Uninstalling

To uninstall the chart with the release name `twofa-helpdesk`:

```console
helm uninstall twofa-helpdesk
```

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | 0.28.0 |

## Values

<table>
	<thead>
		<th>Key</th>
		<th>Type</th>
		<th>Default</th>
		<th>Description</th>
	</thead>
	<tbody>
		<tr>
			<td>additionalAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom annotations to add to all deployed objects.</td>
		</tr>
		<tr>
			<td>additionalLabels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom labels to add to all deployed objects.</td>
		</tr>
		<tr>
			<td>extraIngresses</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.domain</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.environment</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.host</td>
			<td>string</td>
			<td><pre lang="json">
"twofa"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.imageRegistry</td>
			<td>string</td>
			<td><pre lang="json">
"artifacts.software-univention.de"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.podSecurityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.postgresql.connection.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.postgresql.connection.port</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.restartPolicy</td>
			<td>string</td>
			<td><pre lang="json">
"OnFailure"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.securityContext</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>global.tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>imagePullSecrets</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td>Image pull secrets to use for pulling images.</td>
		</tr>
		<tr>
			<td>ingress.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Define custom ingress annotations for all Ingresses.</td>
		</tr>
		<tr>
			<td>ingress.certManager.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td>Enable cert-manager.io annotaion.</td>
		</tr>
		<tr>
			<td>ingress.certManager.issuerRef.kind</td>
			<td>string</td>
			<td><pre lang="json">
"ClusterIssuer"
</pre>
</td>
			<td>Type of Issuer, f.e. "Issuer" or "ClusterIssuer".</td>
		</tr>
		<tr>
			<td>ingress.certManager.issuerRef.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Name of cert-manager.io Issuer resource.</td>
		</tr>
		<tr>
			<td>ingress.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable creation of Ingress.</td>
		</tr>
		<tr>
			<td>ingress.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Define the Fully Qualified Domain Name (FQDN) where application should be reachable. (This will be the default for all Ingresses)</td>
		</tr>
		<tr>
			<td>ingress.ingressClassName</td>
			<td>string</td>
			<td><pre lang="json">
"nginx"
</pre>
</td>
			<td>The Ingress controlledebugr class name. (This will be the default for all Ingresses)</td>
		</tr>
		<tr>
			<td>ingress.items[0].annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[0].enabled</td>
			<td>string</td>
			<td><pre lang="json">
"{{ .Values.twofaHelpdeskFrontend.config.enableAdminHelpdesk }}"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[0].ingressClassName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[0].name</td>
			<td>string</td>
			<td><pre lang="json">
"twofa-helpdesk-ui-admin"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[0].paths</td>
			<td>list</td>
			<td><pre lang="json">
[
  {
    "backend": {
      "service": {
        "name": "2fa-helpdesk-backend-ui",
        "port": {
          "number": 80
        },
        "suffix": "-ui"
      }
    },
    "path": "/univention/2fa/admin",
    "pathType": "Prefix"
  }
]
</pre>
</td>
			<td>Define the Ingress paths.</td>
		</tr>
		<tr>
			<td>ingress.items[0].tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[1].annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[1].enabled</td>
			<td>string</td>
			<td><pre lang="json">
"{{ .Values.twofaHelpdeskFrontend.config.enableSelfService }}"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[1].ingressClassName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[1].name</td>
			<td>string</td>
			<td><pre lang="json">
"twofa-helpdesk-ui-self-service"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[1].paths</td>
			<td>list</td>
			<td><pre lang="json">
[
  {
    "backend": {
      "service": {
        "name": "2fa-helpdesk-backend-ui",
        "port": {
          "number": 80
        },
        "suffix": "-ui"
      }
    },
    "path": "/univention/2fa/self-service",
    "pathType": "Prefix"
  }
]
</pre>
</td>
			<td>Define the Ingress paths.</td>
		</tr>
		<tr>
			<td>ingress.items[1].tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[2]</td>
			<td>object</td>
			<td><pre lang="json">
{
  "annotations": {},
  "enabled": true,
  "ingressClassName": "",
  "name": "twofa-helpdesk-ui-assets",
  "paths": [
    {
      "backend": {
        "service": {
          "name": "2fa-helpdesk-backend-ui",
          "port": {
            "number": 80
          },
          "suffix": "-ui"
        }
      },
      "path": "/univention/2fa/assets",
      "pathType": "Prefix"
    },
    {
      "backend": {
        "service": {
          "name": "2fa-helpdesk-backend-ui",
          "port": {
            "number": 80
          },
          "suffix": "-ui"
        }
      },
      "path": "/univention/2fa/config.json",
      "pathType": "Exact"
    }
  ],
  "tls": {
    "secretName": ""
  }
}
</pre>
</td>
			<td>Shared assets for both admin and self-service UIs</td>
		</tr>
		<tr>
			<td>ingress.items[3].annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].ingressClassName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].name</td>
			<td>string</td>
			<td><pre lang="json">
"twofa-backend"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].paths[0].backend.service.name</td>
			<td>string</td>
			<td><pre lang="json">
"2fa-helpdesk-backend"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].paths[0].backend.service.port.number</td>
			<td>int</td>
			<td><pre lang="json">
8080
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].paths[0].backend.service.suffix</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].paths[0].path</td>
			<td>string</td>
			<td><pre lang="json">
"/backend"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].paths[0].pathType</td>
			<td>string</td>
			<td><pre lang="json">
"Prefix"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.items[3].tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>ingress.tls</td>
			<td>object</td>
			<td><pre lang="json">
{
  "enabled": true,
  "secretName": ""
}
</pre>
</td>
			<td>Secure an Ingress by specifying a Secret that contains a TLS private key and certificate.  Ref.: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls</td>
		</tr>
		<tr>
			<td>ingress.tls.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enable TLS/SSL/HTTPS for Ingress.</td>
		</tr>
		<tr>
			<td>ingress.tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The name of the kubernetes secret which contains a TLS private key and certificate. Hint: This secret is not created by this chart and must be provided.</td>
		</tr>
		<tr>
			<td>keycloak</td>
			<td>object</td>
			<td><pre lang="json">
{
  "admin_realm": "master",
  "auth": {
    "existingSecret": {
      "keyMapping": {
        "adminPassword": null
      },
      "name": null
    },
    "password": "",
    "username": "kcadmin"
  },
  "client": "twofa-helpdesk",
  "connection": {
    "host": "",
    "port": "8080",
    "url": ""
  },
  "realm": ""
}
</pre>
</td>
			<td>Keycloak specific settings.</td>
		</tr>
		<tr>
			<td>keycloak.auth.existingSecret</td>
			<td>object</td>
			<td><pre lang="json">
{
  "keyMapping": {
    "adminPassword": null
  },
  "name": null
}
</pre>
</td>
			<td>Keycloak password secret reference.</td>
		</tr>
		<tr>
			<td>keycloak.auth.password</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Keycloak password.</td>
		</tr>
		<tr>
			<td>keycloak.auth.username</td>
			<td>string</td>
			<td><pre lang="json">
"kcadmin"
</pre>
</td>
			<td>Keycloak user.</td>
		</tr>
		<tr>
			<td>keycloak.client</td>
			<td>string</td>
			<td><pre lang="json">
"twofa-helpdesk"
</pre>
</td>
			<td>Keycloak 2FA client name</td>
		</tr>
		<tr>
			<td>keycloak.connection</td>
			<td>object</td>
			<td><pre lang="json">
{
  "host": "",
  "port": "8080",
  "url": ""
}
</pre>
</td>
			<td>Connection parameters.</td>
		</tr>
		<tr>
			<td>keycloak.connection.host</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Keycloak host (for cluster internal connection of the backend service).</td>
		</tr>
		<tr>
			<td>keycloak.connection.port</td>
			<td>string</td>
			<td><pre lang="json">
"8080"
</pre>
</td>
			<td>Keycloak port.</td>
		</tr>
		<tr>
			<td>keycloak.connection.url</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Keycloak URL (for the helpdesk UI).</td>
		</tr>
		<tr>
			<td>keycloak.realm</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>Keycloak realm.</td>
		</tr>
		<tr>
			<td>keycloakBootstrap.backoffLimit</td>
			<td>int</td>
			<td><pre lang="json">
6
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.config.debug.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.allowPrivilegeEscalation</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.capabilities.drop[0]</td>
			<td>string</td>
			<td><pre lang="json">
"ALL"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.privileged</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.readOnlyRootFilesystem</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.containerSecurityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>keycloakBootstrap.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/keycloak-bootstrap"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"0.20.2@sha256:ee35e620799f269ea54a61b8b1953ff6ed58e8d487298587c32c501c29dadb3b"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.fsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.podSecurityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.resources.limits.cpu</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.resources.limits.memory</td>
			<td>string</td>
			<td><pre lang="json">
"1Gi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.resources.requests.cpu</td>
			<td>float</td>
			<td><pre lang="json">
0.1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.resources.requests.memory</td>
			<td>string</td>
			<td><pre lang="json">
"64Mi"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>keycloakBootstrap.ttlSecondsAfterFinished</td>
			<td>int</td>
			<td><pre lang="json">
60
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>nubusBaseUrl</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.automountServiceAccountToken</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.create</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>serviceAccount.labels</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom labels for the ServiceAccount.</td>
		</tr>
		<tr>
			<td>serviceAccount.name</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.config.twofa_admin_groups[0]</td>
			<td>string</td>
			<td><pre lang="json">
"Domain Admins"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.environment</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/twofa-helpdesk-backend"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.ingress.tls.secretName</td>
			<td>string</td>
			<td><pre lang="json">
"twofa-backend-api-tls"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.podSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.podSecurityContext.fsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.podSecurityContext.fsGroupChangePolicy</td>
			<td>string</td>
			<td><pre lang="json">
"Always"
</pre>
</td>
			<td>Change ownership and permission of the volume before being exposed inside a Pod.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.liveness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.probes.readiness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.resources</td>
			<td>object</td>
			<td><pre lang="json">
{
  "limits": {
    "cpu": "4",
    "memory": "4Gi"
  },
  "requests": {
    "cpu": "250m",
    "memory": "512Mi"
  }
}
</pre>
</td>
			<td>Deployment resources for the backend container</td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.allowPrivilegeEscalation</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.capabilities.drop[0]</td>
			<td>string</td>
			<td><pre lang="json">
"ALL"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.privileged</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.readOnlyRootFilesystem</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.securityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom annotations.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.ports.http.containerPort</td>
			<td>int</td>
			<td><pre lang="json">
8080
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.ports.http.port</td>
			<td>int</td>
			<td><pre lang="json">
8080
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.ports.http.protocol</td>
			<td>string</td>
			<td><pre lang="json">
"TCP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.sessionAffinity.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.sessionAffinity.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
10800
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.service.type</td>
			<td>string</td>
			<td><pre lang="json">
"ClusterIP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskBackend.tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.affinity</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.config.enableAdminHelpdesk</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enables the Ingress for the 2FA admin helpdesk.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.config.enableSelfService</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td>Enables the Ingress for the 2FA self-service.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.config.postLogoutRedirectURI</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td>The URI to redirect the user to after they reset their 2FA token using the self-service helpdesk. If provisioning is active this URL will also be added to the Keycloak clients valid post logout redirect URIs.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.environment</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.fullnameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus-dev/images/twofa-helpdesk-frontend"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Define image sha256 as an alternative to `tag`</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"latest"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.nameOverride</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.nginx.disableIPv6</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.nodeSelector</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podAnnotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podSecurityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podSecurityContext.fsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podSecurityContext.fsGroupChangePolicy</td>
			<td>string</td>
			<td><pre lang="json">
"Always"
</pre>
</td>
			<td>Change ownership and permission of the volume before being exposed inside a Pod.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podSecurityContext.sysctls[0].name</td>
			<td>string</td>
			<td><pre lang="json">
"net.ipv4.ip_unprivileged_port_start"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.podSecurityContext.sysctls[0].value</td>
			<td>string</td>
			<td><pre lang="json">
"1"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.liveness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.failureThreshold</td>
			<td>int</td>
			<td><pre lang="json">
30
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.initialDelaySeconds</td>
			<td>int</td>
			<td><pre lang="json">
20
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.periodSeconds</td>
			<td>int</td>
			<td><pre lang="json">
15
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.successThreshold</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.probes.readiness.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
3
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.replicaCount</td>
			<td>int</td>
			<td><pre lang="json">
1
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.resources</td>
			<td>object</td>
			<td><pre lang="json">
{
  "limits": {
    "cpu": "4",
    "memory": "4Gi"
  },
  "requests": {
    "cpu": "250m",
    "memory": "512Mi"
  }
}
</pre>
</td>
			<td>Deployment resources for the frontend container</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.allowPrivilegeEscalation</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.capabilities.drop[0]</td>
			<td>string</td>
			<td><pre lang="json">
"ALL"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.privileged</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.readOnlyRootFilesystem</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.runAsGroup</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.runAsNonRoot</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.runAsUser</td>
			<td>int</td>
			<td><pre lang="json">
1000
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.securityContext.seccompProfile.type</td>
			<td>string</td>
			<td><pre lang="json">
"RuntimeDefault"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.annotations</td>
			<td>object</td>
			<td><pre lang="json">
{}
</pre>
</td>
			<td>Additional custom annotations.</td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
true
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.ports.http.containerPort</td>
			<td>int</td>
			<td><pre lang="json">
80
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.ports.http.port</td>
			<td>int</td>
			<td><pre lang="json">
80
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.ports.http.protocol</td>
			<td>string</td>
			<td><pre lang="json">
"TCP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.sessionAffinity.enabled</td>
			<td>bool</td>
			<td><pre lang="json">
false
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.sessionAffinity.timeoutSeconds</td>
			<td>int</td>
			<td><pre lang="json">
10800
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.service.type</td>
			<td>string</td>
			<td><pre lang="json">
"ClusterIP"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>twofaHelpdeskFrontend.tolerations</td>
			<td>list</td>
			<td><pre lang="json">
[]
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.pullPolicy</td>
			<td>string</td>
			<td><pre lang="json">
null
</pre>
</td>
			<td>Image pull policy. This setting has higher precedence than global.imagePullPolicy.</td>
		</tr>
		<tr>
			<td>waitForDependency.image.registry</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.repository</td>
			<td>string</td>
			<td><pre lang="json">
"nubus/images/wait-for-dependency"
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.sha256</td>
			<td>string</td>
			<td><pre lang="json">
""
</pre>
</td>
			<td></td>
		</tr>
		<tr>
			<td>waitForDependency.image.tag</td>
			<td>string</td>
			<td><pre lang="json">
"0.36.1@sha256:53a0b3c3a47823aca0a1f99d0d43846316cfef2bf5e35437ee63c8a9468c0296"
</pre>
</td>
			<td></td>
		</tr>
	</tbody>
</table>

