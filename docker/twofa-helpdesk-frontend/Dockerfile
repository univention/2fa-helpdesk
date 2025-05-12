# Stage 1: Build the app
FROM node:20 AS builder

WORKDIR /app

COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/
RUN yarn install

COPY . .
RUN yarn build

# Stage 2: Serve the app
FROM nginx:stable-alpine

# Copy built assets from the previous stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
