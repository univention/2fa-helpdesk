# Usage

    wget http://host:port/backend/openapi.json
    docker build . -t tmp-openapi
    docker run --rm -v "$(pwd):/app" --name tmp-openapi tmp-openapi
    cat README_openapi.md
