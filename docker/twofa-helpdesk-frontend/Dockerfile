# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
ARG UCS_BASE_IMAGE_TAG=5.2.2-build.20250714
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

###############################################################################
# Step 0: Prepare builder image
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS local-dev-env

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG NODE_VERSION="20.19.3"
ARG YARN_VERSION="1.22.19"
ARG NODE_SHA256="76272878069683c3a36b933d2f4842436a26b527daa930ae9346b477011ee2f3"

# The following dependencies are only needed when on an aarch64 platform,
# because then the package "deasync" does not include ready made binaries
# for the platform and falls back to compiling them.
#
# This is relevant for developers who work on machines with Apple's M1
# processors.

# hadolint ignore=DL3008
RUN \
    apt-get install  --assume-yes --verbose-versions --no-install-recommends \
    "ca-certificates" \
    "wget" \
    && if [[ "$(uname -m)" == "aarch64" ]]; then \
    apt-get --assume-yes --verbose-versions --no-install-recommends install \
    "gcc" \
    "g++" \
    "make" \
    "python3" \
    ; fi \
    && wget --progress="dot:giga" --output-document="node.tar.gz" \
    "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" \
    && echo "${NODE_SHA256}  node.tar.gz" > SHA256 \
    && sha256sum --check "SHA256" \
    && tar xz -C "/usr/local" --strip-components=1 -f "node.tar.gz" \
    && rm -f "node.tar.gz" "SHA256" \
    && NODE_RESULT=$(node --version) \
    && echo "node version: ${NODE_RESULT}" \
    && if [[ "${NODE_RESULT}" != "v${NODE_VERSION}" ]]; then echo "Bad node version"; exit 1; fi \
    && npm install -g yarn@"${YARN_VERSION}" \
    && yarn set version "${YARN_VERSION}" \
    && YARN_RESULT=$(yarn --version) \
    && echo "yarn version: ${YARN_RESULT}" \
    && if [[ "${YARN_RESULT}" != "${YARN_VERSION}" ]]; then echo "Bad yarn version"; exit 1; fi

WORKDIR /app
CMD ["/bin/bash"]

FROM local-dev-env AS base
COPY ./package.json .
COPY ./yarn.lock .

RUN \
    yarn install --frozen-lockfile \
    && yarn cache clean

# Copy should come after yarn install to prevent long rebuilding time
COPY . .

###############################################################################
# Step 1: Build the app
FROM base AS build

RUN yarn build

###############################################################################
# Step 2: Serve with nginx
FROM gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/nginx/nginx:0.4.1 AS final

# RUN apk add python3
RUN apt-get update && \
    apt-get install --assume-yes --verbose-versions --no-install-recommends python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=build /app/dist /usr/share/nginx/html/ui

COPY 90_generate_config.py /
COPY 90_generate_config.sh /entrypoint.d/
