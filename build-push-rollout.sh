#!/bin/bash

if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

VERSION=${VERSION:-local}
IMAGE_NAME="${IMAGE_NAME}:${VERSION}"

docker build --build-arg VERSION=${VERSION} -t ${IMAGE_NAME} app
docker push ${IMAGE_NAME}

kubectl set image deployment/flask-test flask-test=${IMAGE_NAME} --record 
kubectl rollout status deployment.v1.apps/flask-test
kubectl rollout history deployment/flask-test
