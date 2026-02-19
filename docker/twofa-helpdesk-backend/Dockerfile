# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.4-build.20260108@sha256:97b04d50531636aa2e30e915b38e3daacea1e49b58774daa97f9d698e6855a93
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG POETRY_VERSION=2.1.3

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS builder

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    curl \
    python3-pip \
    python3-univention-directory-manager-rest-client \
    python3-venv \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ARG POETRY_VERSION
ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=${POETRY_VERSION}
RUN python3 -m venv "$POETRY_HOME" \
    && "$POETRY_HOME"/bin/pip install --no-cache-dir poetry==${POETRY_VERSION}
ENV PATH="$POETRY_HOME/bin:$PATH"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY ./src/poetry.lock ./src/pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --only=main --no-root

COPY ./src ./src

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --only-root

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS runtime

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    python3 \
    python3-univention-directory-manager-rest-client \
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
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src:/usr/lib/python3/dist-packages"

USER ${USER}

WORKDIR /app/src/2fa_helpdesk

CMD ["uvicorn", "app:app", "--proxy-headers", "--forwarded-allow-ips", "*", "--port", "8080", "--host", "0.0.0.0"]
