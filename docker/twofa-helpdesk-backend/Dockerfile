# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=0.18.0
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-521

ARG WORKDIR="/src"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
ARG WORKDIR
WORKDIR ${WORKDIR}

ARG USER=fastapi
RUN useradd -m "$USER"

COPY ./src/poetry.lock ${WORKDIR}
COPY ./src/pyproject.toml ${WORKDIR}

RUN chown -R "$USER":"$USER" "${WORKDIR}"

RUN chown "$USER":"$USER" "$WORKDIR" \
    && apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
      python3-pip \
      python3-univention-directory-manager-rest-client \
      curl \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV \
    PATH="/home/${USER}/.local/bin:${PATH}" \
    PYTHONPATH="." \
    WEB_CONCURRENCY=1 \
    # Do not buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Do not create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1 \
    # Do not ask questions
    POETRY_NO_INTERACTION=1 \
    # Put .venv inside source folder
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # Cache of poetry
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # Include system site packages
    PYTHONPATH=.:/usr/lib/python3/dist-packages/

# install Poetry
RUN pip3 install --break-system-packages --no-cache-dir poetry>=1.7.0
RUN poetry --version

COPY ./src ${WORKDIR}
RUN chown -R "$USER":"$USER" "${WORKDIR}"

# copy source code and install project
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN poetry config virtualenvs.create false
RUN poetry install #--only main

WORKDIR /src/2fa_helpdesk
CMD ["uvicorn", "app:app", "--proxy-headers", "--root-path", "./", "--port", "8080", "--host", "0.0.0.0"]
