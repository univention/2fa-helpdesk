# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261112@sha256:519c50da25332623a7a30d911965f13cd333e4b9b1402036e5bb4dd85d98f6c6
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

###############################################################################
# Step 0: Prepare builder image
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS local-dev-env

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG PNPM_VERSION="12.15.0"

# Debian's Node 20 is too old for jsdom.
COPY --from=docker.io/library/node:24.15.0-trixie-slim@sha256:291be77873bc04731968cacf82f0fcef17cee8cf200c6b6951e2bcab41560eb7 /usr/local/bin/node /usr/local/bin/node
COPY --from=docker.io/library/node:24.15.0-trixie-slim@sha256:291be77873bc04731968cacf82f0fcef17cee8cf200c6b6951e2bcab41560eb7 /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm

# hadolint ignore=DL3008
RUN \
    apt-get install  --assume-yes --verbose-versions --no-install-recommends \
    "ca-certificates" \
    && node /usr/local/lib/node_modules/npm/bin/npm-cli.js install -g pnpm@"${PNPM_VERSION}" \
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
