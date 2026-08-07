# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

FROM node:24-alpine@sha256:d32cdf619f63fe0471182d08996dd516c6275bb5fd31ae06e55a570bd9e1ad43

WORKDIR /app

RUN npm install -g widdershins
RUN apk add wget

COPY openapi.json .
CMD ["widdershins", "openapi.json", "--omitHeader", "--omitBody", "--language_tabs=[]", "-o", "README_openapi.md"]
