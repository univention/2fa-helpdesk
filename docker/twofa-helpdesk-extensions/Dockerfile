# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.5-build.20260417@sha256:01d93ca22e4312a1d3d47322bc93448e5cf0b55206ec5b3e019493f632debe36
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY /extensions/plugins/udm/udm-data-loader /plugins/udm-data-loader
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

CMD ["/bin/loader"]
