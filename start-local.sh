#!/bin/bash

VERSION=local
IMAGE_NAME="flask-test"

docker build --build-arg VERSION=${VERSION} -t ${IMAGE_NAME} app

docker run -ti -p 8000:8000 \
    --name=flask-test-container \
    --rm \
    -e WORKERS=3 \
    -e STAGE=local \
    -e JWT_DEFAULT_REALM=test \
    ${IMAGE_NAME}
