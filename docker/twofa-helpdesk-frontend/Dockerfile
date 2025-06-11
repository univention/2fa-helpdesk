# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

# Step 1: Build the app
FROM node:20-alpine AS builder

WORKDIR /app
COPY ./frontend .
RUN yarn install --frozen-lockfile && yarn build

# Step 2: Serve with nginx
FROM nginx:stable-alpine

RUN apk add --no-cache python3=3.12.11-r0

COPY --from=builder /app/dist /usr/share/nginx/html/ui

COPY frontend/90_generate_config.py /
COPY frontend/90_generate_config.sh /docker-entrypoint.d/

# Set up nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
