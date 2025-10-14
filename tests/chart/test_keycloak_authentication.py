# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import (
    AuthPasswordUsageViaEnv, AuthPasswordUsageViaVolume)
from univention.testing.helm.auth_flavors.secret_generation import \
    AuthSecretGenerationUser
from univention.testing.helm.auth_flavors.username import \
    AuthUsernameViaConfigMap


class SettingsTestKeycloakSecret:
    secret_name = "release-name-twofa-helpdesk-keycloak-credentials"
    prefix_mapping = {"keycloak.auth": "auth"}

    path_password = "stringData.adminPassword"

    # for AuthPasswordUsageViaEnv and AuthPasswordUsageViaVolume
    sub_path_env_password = "env[?@name=='KEYCLOAK_PASSWORD']"
    secret_default_key = "adminPassword"

    # for AuthUsername and AuthUsernameViaConfigMap
    path_username = "data.KEYCLOAK_USERNAME"
    default_username = "kcadmin"


class TestChartCreatesKeycloakSecretAsUser(SettingsTestKeycloakSecret,
                                           AuthSecretGenerationUser):
    pass


class Test2faBackendUsesKeycloakCredentialsByEnv(SettingsTestKeycloakSecret,
                                                 AuthPasswordUsageViaEnv):
    workload_name = "release-name-twofa-helpdesk"


class TestKeycloakBootstrapUsesKeycloakCredentialsByEnv(SettingsTestKeycloakSecret,
                                                        AuthPasswordUsageViaEnv):
    workload_name = "release-name-twofa-helpdesk-1-keycloak-bootstrap"
    workload_kind = "Job"


class TestKeycloakBootstrapUsesKeycloakCredentialsByVolume(SettingsTestKeycloakSecret,
                                                           AuthPasswordUsageViaVolume):
    workload_name = "release-name-twofa-helpdesk-1-keycloak-bootstrap"
    workload_kind = "Job"
    volume_name = "keycloak-credentials-volume"


class TestKeycloakBootstrapUsesKeycloakUsernameFromConfigMap(SettingsTestKeycloakSecret,
                                                             AuthUsernameViaConfigMap):
    workload_name = "release-name-twofa-helpdesk-1-keycloak-bootstrap"
    config_map_name = "release-name-twofa-helpdesk-keycloak-bootstrap-env"


class Test2faBackendUsesKeycloakUsernameFromConfigMap(SettingsTestKeycloakSecret,
                                                      AuthUsernameViaConfigMap):
    workload_name = "release-name-twofa-helpdesk"
    config_map_name = "release-name-twofa-helpdesk-config"
