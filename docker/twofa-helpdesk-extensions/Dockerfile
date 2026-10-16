# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261008@sha256:52175e1efb9452119ed135126afd931d4e2361bdc69bded46101e35fa27ae0d0
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY /extensions/plugins/udm/udm-data-loader /plugins/udm-data-loader
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

CMD ["/bin/loader"]
