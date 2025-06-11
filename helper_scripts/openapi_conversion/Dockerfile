# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

FROM node:18-alpine

WORKDIR /app

RUN npm install -g widdershins
RUN apk add wget

COPY openapi.json .
CMD ["widdershins", "openapi.json", "--omitHeader", "--omitBody", "--language_tabs=[]", "-o", "README_openapi.md"]
