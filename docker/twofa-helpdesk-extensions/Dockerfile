# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.5-build.20260326@sha256:8381ca70cdad990e82dd44a9cb58a04be22cef60ef50a025a42a7620dcb09a9e
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY /extensions/plugins/udm/udm-data-loader /plugins/udm-data-loader
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

CMD ["/bin/loader"]
