# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python
ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261022@sha256:ea444eeecf1681d2ca6e599a08779b3e078a29311f74678b2a3245474c564f61
ARG UCS_DISTROLESS_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-distroless-python
ARG UCS_DISTROLESS_IMAGE_TAG=5.3.0-build.20261022@sha256:f65cefc852c76dfd42ad0c1ad0f6885357e62899f51aa421b6f89eef550b97cf

###############################################
# Stage 1: build the virtual environment
#
# Built on ucs-base-python so the venv is made by the same CPython minor
# version the distroless final stage runs.
FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.13@sha256:b485bd65cc2cf1c9a93b3554012c9c3778cf7b1b5fd3d3096ce9e1226c97e1e6 /uv /usr/local/bin/uv

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
