# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20260903@sha256:c0c06ea1ef4aa8fea856581ecb2ed7f9fc6b355c3f0903a1be39f02a5472dfd5
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

###############################################################################
# Step 0: Prepare builder image
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS local-dev-env

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG NODE_VERSION="24.15.0"
ARG YARN_VERSION="1.22.22"
ARG NODE_SHA256="44836872d9aec49f1e6b52a9a922872db9a2b02d235a616a5681b6a85fec8d89"

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
COPY ./frontend/package.json .
COPY ./frontend/yarn.lock .

RUN \
    yarn install --frozen-lockfile \
    && yarn cache clean

# Copy should come after yarn install to prevent long rebuilding time
COPY ./frontend .

###############################################################################
# Step 1: Build the app
FROM base AS build

RUN yarn build

###############################################################################
# Step 2: Serve with nginx
FROM gitregistry.knut.univention.de/univention/dev/nubus-for-k8s/nginx/nginx:0.7.47@sha256:d3ae9dc6345e364841b51c01b008576e11c5b1b4b7c0481b592d1ed79fec4c12 AS final

# RUN apk add python3
RUN apt-get update && \
    apt-get install --assume-yes --verbose-versions --no-install-recommends python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=build /app/dist /usr/share/nginx/html/univention/2fa

COPY frontend/90_generate_config.py /
COPY frontend/90_generate_config.sh /entrypoint.d/

FROM final AS sbom

COPY ./sbom-fs-frontend.cdx.json /
