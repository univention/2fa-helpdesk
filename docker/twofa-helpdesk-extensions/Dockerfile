# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20260924@sha256:24c09705ee51cd38b3659afb52799069d3a8ec5514a916b7e62e9fbf7f58c0a4
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY /extensions/plugins/udm/udm-data-loader /plugins/udm-data-loader
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

CMD ["/bin/loader"]
