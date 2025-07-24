# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.base import Base
from pytest_helm.utils import load_yaml
from pytest_helm.helm import Helm


class TestTemplateConditionalIngress(Base):
    template_name = "templates/ingress.yaml"
    admin_ingress_name = "release-name-twofa-helpdesk-twofa-helpdesk-ui-admin"
    self_service_ingress_name = "release-name-twofa-helpdesk-twofa-helpdesk-ui-self-service"

    def _assert_ingress_present(self, ingresses: list, ingress_name: str):
        ingress_names = [ing["metadata"]["name"] for ing in ingresses]
        assert any(ingress_name == name for name in ingress_names), (
            f"Expected ingress '{ingress_name}' not found in: {ingress_names}"
        )

    def _assert_ingress_absent(self, ingresses: list, ingress_name: str):
        ingress_names = [ing["metadata"]["name"] for ing in ingresses]
        assert not any(ingress_name == name for name in ingress_names), (
            f"Unexpected ingress '{ingress_name}' found in: {ingress_names}"
        )

    def _assert_ingress_count(self, ingresses: list, expected_count: int):
        actual_count = len(ingresses)
        assert actual_count == expected_count, (
            f"Expected {expected_count} ingresses, got {actual_count}. "
            f"Ingresses: {[ing['metadata']['name'] for ing in ingresses]}"
        )

    def helm_template_file(
        self,
        helm: Helm,
        chart,
        values: dict,
        template_file: str,
        helm_args: list[str] | None = None,
    ) -> list:
        assert template_file

        result = helm.helm_template(chart, values, template_file, helm_args)
        return result

    def test_disable_ingress_admin_ingress(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableAdminHelpdesk: false
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )
        self._assert_ingress_absent(ingresses, self.admin_ingress_name)
        self._assert_ingress_count(ingresses, 2)

    def test_disable_ingress_self_service_ingress(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableSelfService: false
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )
        self._assert_ingress_absent(ingresses, self.self_service_ingress_name)
        self._assert_ingress_count(ingresses, 2)

    def test_disable_ingress_ui(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableSelfService: false
                    enableAdminHelpdesk: false
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )
        self._assert_ingress_absent(ingresses, self.self_service_ingress_name)
        self._assert_ingress_absent(ingresses, self.admin_ingress_name)
        self._assert_ingress_count(ingresses, 1)

    def test_enable_ingress_ui(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableSelfService: true
                    enableAdminHelpdesk: true
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )
        self._assert_ingress_present(ingresses, self.self_service_ingress_name)
        self._assert_ingress_present(ingresses, self.admin_ingress_name)
        self._assert_ingress_count(ingresses, 3)

    def test_template_null(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableSelfService: null
                    enableAdminHelpdesk: null
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )

        self._assert_ingress_absent(ingresses, self.self_service_ingress_name)
        self._assert_ingress_absent(ingresses, self.admin_ingress_name)
        self._assert_ingress_count(ingresses, 1)

    def test_template_empty_string(self, helm, chart_path):
        values = load_yaml(
            """
            twofaHelpdeskFrontend:
                config:
                    enableSelfService: ""
                    enableAdminHelpdesk: ""
            """,
        )

        ingresses = self.helm_template_file(
            helm,
            chart_path,
            values,
            self.template_name,
        )

        self._assert_ingress_absent(ingresses, self.self_service_ingress_name)
        self._assert_ingress_absent(ingresses, self.admin_ingress_name)
        self._assert_ingress_count(ingresses, 1)
