# Step 1: Build the app
FROM node:20-alpine AS builder
WORKDIR /app
COPY ./frontend .
RUN yarn install --frozen-lockfile && yarn build

# Step 2: Serve with nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html/ui

# Set up nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
