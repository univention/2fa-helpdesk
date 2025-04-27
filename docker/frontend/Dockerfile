# Stage 1: Build the app
FROM node:20 AS builder

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

# Stage 2: Serve the app
FROM nginx:stable-alpine

# Copy built assets from the previous stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config (optional, to disable caching etc.)
# COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "pid /var/cache/nginx/nginx.pid; daemon off;"]
