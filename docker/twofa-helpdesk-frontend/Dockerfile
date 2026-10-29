# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261026@sha256:20df13170832602bed0c2cf83393eb0a31eb1864c86f86e079c6d3a9271974ab
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

###############################################################################
# Step 0: Prepare builder image
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS local-dev-env

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG NODE_VERSION="24.15.0"
ARG PNPM_VERSION="12.15.0"
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
    && npm install -g pnpm@"${PNPM_VERSION}" \
    && PNPM_RESULT=$(pnpm --version) \
    && echo "pnpm version: ${PNPM_RESULT}" \
    && if [[ "${PNPM_RESULT}" != "${PNPM_VERSION}" ]]; then echo "Bad pnpm version"; exit 1; fi

WORKDIR /app
CMD ["/bin/bash"]

FROM local-dev-env AS base
COPY ./frontend/package.json .
COPY ./frontend/pnpm-lock.yaml .
COPY ./frontend/pnpm-workspace.yaml .

RUN pnpm install --frozen-lockfile

# Copy should come after pnpm install to prevent long rebuilding time
COPY ./frontend .

###############################################################################
# Step 1: Build the app
FROM base AS build

RUN pnpm build

###############################################################################
# Step 2: Serve with nginx
FROM gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-nginx:5.3.0-build.20261102@sha256:7fdda30d248ef37a1ab8f5eb6c183df54bd87f0f7aaad5f704afe5552cdaede1 AS final

COPY --from=build /app/dist /usr/share/nginx/html/univention/2fa

FROM final AS sbom

COPY ./sbom-fs-frontend.cdx.json /
