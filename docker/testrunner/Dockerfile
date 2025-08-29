# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023-2025 Univention GmbH

ARG DOCKER_PROXY

# TODO: The usage of just "3.13" causes issues since Playwright is not yet
# supporting changed package names in the latest Debian release.
#
# See: https://github.com/microsoft/playwright-python/issues/2950
ARG PYTHON_TAG=3.13-slim-bookworm

# NOTE: "base-env" helps to enter the clean environment in docker so that it is
# possible to run "pipenv lock" from inside the container.
FROM ${DOCKER_PROXY}python:${PYTHON_TAG} AS base-env

WORKDIR /testrunner

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv==2023.6.18


FROM base-env
RUN pipenv sync --dev --system \
    && rm -r ~/.cache \
    && playwright install-deps \
    && playwright install chromium

WORKDIR /app

CMD [ "pytest", "tests/integration/api-2fa" ]
