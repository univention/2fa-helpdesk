# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 - 2025 Univention GmbH

ARG BASE_IMAGE_TAG=3.20
ARG BASE_IMAGE=docker.io/alpine
FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG}

WORKDIR /

# Copy plugins of the packaged integration to the Docker image
COPY ./extensions/plugins /plugins
# Copy the plugin loader to the Docker image
COPY /extensions/loader.sh /bin/loader

RUN chmod -R a+rwX /plugins
RUN chmod a+rx /bin/loader

RUN addgroup -S appgroup
RUN adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /plugins
USER appuser

CMD ["/bin/loader"]
