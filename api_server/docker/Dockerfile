FROM ubuntu:22.04

#######################################
# Dockerfile for production !
#######################################

# Var for labels
ARG GITHUB_ACTOR
ARG GITHUB_REPOSITORY
ARG GITHUB_REF

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

ENV PROJECT_NAME="PurpleCaffeine"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV env="prod"

LABEL org.opencontainers.image.title="${PROJECT_NAME}" \
      org.opencontainers.image.authors=${GITHUB_ACTOR} \
      org.opencontainers.image.vendor=${GITHUB_REPOSITORY} \
      org.opencontainers.image.source="https://github.com/${GITHUB_ACTOR}/purplecaffeine" \
      org.opencontainers.image.url="https://github.com/${GITHUB_ACTOR}/purplecaffeine/tags" \
      org.opencontainers.image.description="API for quantum experiment tracking." \
      org.opencontainers.image.os="Ubuntu" \
      org.opencontainers.image.version=${GITHUB_REF}

RUN apt-get update -yq \
&& apt-get install python3-pip -y

COPY core/ /opt/api_server/core
COPY purplecaffeine/ /opt/api_server/purplecaffeine
COPY manage.py /opt/api_server/
COPY requirements.txt /opt/api_server/

RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r /opt/api_server/requirements.txt

EXPOSE 8000

CMD cd /opt/api_server; \
    python3 manage.py makemigrations core; \
    python3 manage.py migrate; \
    gunicorn --bind 0.0.0.0:8000 purplecaffeine.wsgi
