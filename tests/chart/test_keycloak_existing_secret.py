# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
# ruff: noqa: E501

from subprocess import CalledProcessError

from pytest_helm.utils import load_yaml
from univention.testing.helm.deployment import Base


class TemplateError:
    kc_default_name_created_secret = "release-name-twofa-helpdesk-keycloak-credentials"
    kc_default_key_created_secret = "adminPassword"
    kc_default_key_existing_secret = "adminPassword"
    kc_custom_name_existing_secret = "custom-keycloak-credentials"
    kc_custom_key_existing_secret = "custom_admin_password"

    def assert_templating_fails(self, helm, chart_path, values):
        try:
            manifest = self.helm_template_file(helm, chart_path, values, self.template_file)
        except CalledProcessError:
            return
        assert False, "Expected CalledProcessError but got a manifest: {}".format(manifest)

class KeycloakExistingSecret(Base, TemplateError):

    def test_use_created_secret_if_password_is_given_and_existing_secret_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: "default_password"
                existingSecret: null
            """,
            ),
        )
        self.assert_created_secret_is_used(helm, chart_path, values)


    def test_use_created_secret_if_password_is_given_and_existing_secret_name_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: "default_password"
                existingSecret:
                    name: null
            """,
            ),
        )
        self.assert_created_secret_is_used(helm, chart_path, values)

    def test_use_created_secret_if_password_is_given_and_existing_secret_name_is_empty(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: "default_password"
                existingSecret:
                    name: ""
            """,
            ),
        )
        self.assert_created_secret_is_used(helm, chart_path, values)

    def test_use_default_key_of_existing_secret_if_key_mapping_is_empty(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                f"""
            keycloak:
              auth:
                existingSecret:
                    name: "{self.kc_custom_name_existing_secret}"
                    keyMapping:
                        adminPassword: ""
            """,
            ),
        )
        self.assert_default_key_mapping_is_used(helm, chart_path, values)

    def test_use_default_key_of_existing_secret_if_key_mapping_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                f"""
            keycloak:
              auth:
                existingSecret:
                    name: "{self.kc_custom_name_existing_secret}"
                    keyMapping:
                        adminPassword: null
            """,
            ),
        )
        self.assert_default_key_mapping_is_used(helm, chart_path, values)

    def test_use_complete_existing_secret_if_name_and_key_mapping_are_given(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                f"""
            keycloak:
              auth:
                existingSecret:
                    name: "{self.kc_custom_name_existing_secret}"
                    keyMapping:
                        adminPassword: "{self.kc_custom_key_existing_secret}"
            """,
            ),
        )
        self.assert_correct_secret_key_ref_is_used(helm, chart_path, values,
                                    self.kc_custom_name_existing_secret,
                                    self.kc_custom_key_existing_secret)


    def assert_correct_secret_key_ref_is_used(self, helm, chart_path, values, secret_name, secret_key):
        deployment = self.helm_template_file(helm, chart_path, values, self.template_file)
        env = deployment["spec"]["template"]["spec"]["containers"][0]["env"]
        kc_env = next((e for e in env if e.get("name") == "KEYCLOAK_PASSWORD"), None)

        assert kc_env is not None, "KEYCLOAK_PASSWORD env var is missing"
        assert kc_env["valueFrom"]["secretKeyRef"]["name"] == secret_name
        assert kc_env["valueFrom"]["secretKeyRef"]["key"] == secret_key

    def assert_created_secret_is_used(self, helm, chart_path, values):
        self.assert_correct_secret_key_ref_is_used(helm, chart_path, values,
                                            self.kc_default_name_created_secret,
                                            self.kc_default_key_created_secret)

    def assert_default_key_mapping_is_used(self, helm, chart_path, values):
        self.assert_correct_secret_key_ref_is_used(helm, chart_path, values,
                                            self.kc_custom_name_existing_secret,
                                            self.kc_default_key_existing_secret)



class TestKeycloakSecretCreation(Base, TemplateError):
    template_file = "templates/secret-keycloak.yaml"

    def test_fail_if_neither_password_nor_existing_secret_name_is_given_when_auth_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth: null
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_fail_if_neither_password_nor_existing_secret_name_is_given_when_both_are_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: null
                existingSecret: null
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_fail_if_neither_password_nor_existing_secret_name_is_given_when_password_is_empty(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: ""
                existingSecret: null
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_fail_if_neither_password_nor_existing_secret_name_is_given_when_existing_secret_name_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: ""
                existingSecret:
                    name: null
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_fail_if_neither_password_nor_existing_secret_name_is_given_when_existing_secret_name_is_empty(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: ""
                existingSecret:
                    name: ""
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_fail_if_existing_secret_name_is_given_but_key_mapping_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                f"""
            keycloak:
              auth:
                existingSecret:
                    name: "{self.kc_custom_name_existing_secret}"
                    keyMapping: null
            """,
            ),
        )
        self.assert_templating_fails(helm, chart_path, values)

    def test_secret_is_created_if_password_is_given_and_existing_secret_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: "default_password"
                existingSecret: null
            """,
            ),
        )
        self.assert_secret_is_created_as_expected(helm, chart_path, values)

    def test_secret_is_created__if_password_is_given_and_existing_secret_name_is_null(self, helm, chart_path):
        values = self.add_prefix(
            load_yaml(
                """
            keycloak:
              auth:
                password: "default_password"
                existingSecret:
                    name: null
            """,
            ),
        )
        self.assert_secret_is_created_as_expected(helm, chart_path, values)

    def assert_secret_is_created_as_expected(self, helm, chart_path, values):
        secret = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert secret["kind"] == "Secret", "Expected a Secret kind"
        assert secret["metadata"]["name"] == self.kc_default_name_created_secret, "Unexpected secret name"
        assert self.kc_default_key_created_secret in secret["stringData"], f"Expected {self.kc_default_key_created_secret} in stringData"
        assert secret["stringData"][self.kc_default_key_created_secret] == "default_password", "Unexpected password in stringData"

class TestKeycloakSecretInDeployment(KeycloakExistingSecret):
    template_file = "templates/deployment.yaml"

class TestKeycloakSecretInJobProvisioning(KeycloakExistingSecret):
    template_file = "templates/job-provisioning.yaml"
