# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2026 Univention GmbH

ARG DOCKER_PROXY

# TODO: The usage of just "3.13" causes issues since Playwright is not yet
# supporting changed package names in the latest Debian release.
#
# See: https://github.com/microsoft/playwright-python/issues/2950
ARG PYTHON_TAG=3.13-slim-bookworm

# NOTE: "base-env" helps to enter the clean environment in docker so that it is
# possible to run "uv lock" from inside the container.
FROM ${DOCKER_PROXY}python:${PYTHON_TAG} AS base-env

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /testrunner

COPY pyproject.toml uv.lock ./


FROM base-env

# Playwright defaults to ~/.cache/ms-playwright, which the cache mount below would keep out of the image.
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# The node binary that Playwright bundles needs libatomic1 before install-deps can run.
# hadolint ignore=DL3008
RUN --mount=type=cache,target=/root/.cache \
    apt-get update \
    && apt-get install --assume-yes --no-install-recommends libatomic1 \
    && rm -rf /var/lib/apt/lists/* \
    && uv sync --locked \
    && playwright install-deps \
    && playwright install chromium

WORKDIR /app

CMD [ "pytest", "tests/integration/api-2fa" ]
