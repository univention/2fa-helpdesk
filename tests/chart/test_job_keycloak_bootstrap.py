# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH


class TestJobKeycloakBootstrap:

    template_file = "templates/job-keycloak-bootstrap.yaml"

    job_name = "release-name-twofa-helpdesk-1-keycloak-bootstrap"

    def test_pod_name_label_is_unique_and_stable(self, chart):
        result = chart.helm_template(None, self.template_file)
        job = result.get_resource(kind="Job", name=self.job_name)
        labels = job.findone("spec.template.metadata.labels")
        assert labels["app.kubernetes.io/name"] == "release-name-twofa-helpdesk-keycloak-bootstrap"
