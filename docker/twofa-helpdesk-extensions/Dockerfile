# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20260824@sha256:e2b7ee0b179cd4a2a2610e9e9cc412b5452bd4a8bcd3ae791a1f498af64d1566
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY /extensions/plugins/udm/udm-data-loader /plugins/udm-data-loader
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

CMD ["/bin/loader"]
