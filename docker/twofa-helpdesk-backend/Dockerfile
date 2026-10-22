# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261008@sha256:52175e1efb9452119ed135126afd931d4e2361bdc69bded46101e35fa27ae0d0
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

###############################################
# Stage 1: build the virtual environment
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS builder

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    python3 \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY --from=ghcr.io/astral-sh/uv:0.12.13@sha256:b485bd65cc2cf1c9a93b3554012c9c3778cf7b1b5fd3d3096ce9e1226c97e1e6 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY ./src/pyproject.toml ./src/uv.lock ./

# The project is not packaged, so this installs the dependencies and nothing
# else. The sources are copied in below and run from /app/src.
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev

COPY ./src ./src

# Verify the app imports while a shell is still available; the final stage has
# none. app.py builds its OIDC settings at import time, hence the three
# variables. Nothing contacts those URLs, PyJWKClient fetches lazily.
RUN OIDC_HOST=http://localhost OIDC_REALM=verify OIDC_CLIENT_ID=verify \
    /app/.venv/bin/python -c 'import sys; sys.path.insert(0, "/app/src/2fa_helpdesk"); import app'

###############################################
# Stage 2: final image
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS runtime

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    python3 \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ARG USER=fastapi
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} ${USER} \
    && useradd -l -m -u ${UID} -g ${GID} -s /bin/bash ${USER}

WORKDIR /app

COPY --from=builder --chown=root:root --chmod=755 /app/.venv /app/.venv
COPY --from=builder --chown=root:root --chmod=755 /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER ${USER}

EXPOSE 8080

CMD ["/app/.venv/bin/uvicorn", "--app-dir", "/app/src/2fa_helpdesk", "app:app", \
     "--proxy-headers", "--forwarded-allow-ips", "*", "--port", "8080", "--host", "0.0.0.0"]
