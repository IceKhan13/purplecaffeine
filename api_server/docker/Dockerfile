FROM ubuntu:22.04

# Var for labels
ARG GITHUB_ACTOR
ARG GITHUB_REPOSITORY
ARG GITHUB_REF

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

ENV PROJECT_NAME="PurpleCaffeine"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

COPY api_server/code/ /opt/api_server/core
COPY api_server/purplecaffeine /opt/api_server/purplecaffeine
COPY api_server/requirements.txt /opt/api_server/
COPY api_server/docker/start.sh /opt/

RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r /opt/api_server/requirements.txt

EXPOSE 8000

# I don't know how to launch Django without the webserver
CMD ["python3", "manage.py", "", "0.0.0.0:8000"]
