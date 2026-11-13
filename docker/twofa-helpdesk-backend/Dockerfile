# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261112@sha256:25e5e183b1b4f75c64e0c697d5795a8e9c15b935453c2a64406d7d1ab40b2214
ARG UCS_DISTROLESS_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20261112@sha256:c4766a3c4624d2173f1b39da3be5088c90e64564ce0fccf14f9106ee83fb422c

###############################################
# Stage 1: build the virtual environment
#
# Built on ucs-base-python so the venv is made by the same CPython minor
# version the distroless final stage runs.
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

COPY ./src/pyproject.toml ./src/uv.lock ./

# Dependencies first, so editing a source file does not reinstall them.
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev --no-install-project

COPY ./src/twofa_helpdesk ./twofa_helpdesk

# --no-editable puts a built copy of the package inside the venv, so the final
# stage needs nothing but /app/.venv.
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev --no-editable \
    && uv export --no-dev --frozen --no-emit-project --no-hashes -o /app/requirements.txt

###############################################
# Stage 2: final image
#
# Distroless: no shell, so every instruction here is exec form. The user and
# the CA bundle come from the base image.
FROM ${UCS_DISTROLESS_IMAGE}:${UCS_DISTROLESS_IMAGE_TAG} AS runtime

EXPOSE 8080

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/requirements.txt /app/requirements.txt

WORKDIR /app

# Verify the app imports in the image that ships. app.py builds its OIDC
# settings at import time, hence the three variables. Nothing contacts those
# URLs, PyJWKClient fetches lazily. hadolint shellchecks the Python as sh.
# hadolint ignore=SC1072
RUN ["python3.13", "-c", \
     "import os; os.environ.update(OIDC_HOST='http://localhost', OIDC_REALM='verify', OIDC_CLIENT_ID='verify'); import twofa_helpdesk.app"]

# The base image ships an ENTRYPOINT of its own, which would swallow CMD.
ENTRYPOINT []

CMD ["/app/.venv/bin/uvicorn", "twofa_helpdesk.app:app", \
     "--proxy-headers", "--forwarded-allow-ips", "*", "--port", "8080", "--host", "0.0.0.0"]
