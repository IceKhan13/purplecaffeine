#!/bin/bash

echo "================================================================="
echo "Django Installer!!"
echo "================================================================="

source ../.envrc
export DB_HOST=host.docker.internal

echo "================================================================="
echo "Build image"
echo "================================================================="

docker build . -f docker/Dockerfile.dev --tag purplecaffeine:dev

echo "================================================================="
echo "Launch Django"
echo "================================================================="

docker rm -f purplecaffeine-dev 2> /dev/null
docker run --rm --name purplecaffeine-dev \
    -p 8000:8000 \
    -v "$PWD":/opt/api_server \
    -e SERV_KEY="${SERV_KEY}" \
    -e DB_NAME="${DB_NAME}" -e DB_USER="${DB_USER}" -e DB_PASSWORD="${DB_PASSWORD}" \
    -e DB_SCHEMA="${DB_SCHEMA}" -e DB_PORT="${DB_PORT}" -e DB_HOST="${DB_HOST}" \
    -e DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}" -e DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}" \
    -e DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}" \
    purplecaffeine:dev
