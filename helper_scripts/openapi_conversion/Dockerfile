FROM node:18-alpine

WORKDIR /app

RUN npm install -g widdershins
RUN apk add wget

COPY openapi.json .
CMD ["widdershins", "openapi.json", "--omitHeader", "--omitBody", "--language_tabs=[]", "-o", "README_openapi.md"]
