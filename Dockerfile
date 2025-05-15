FROM python:3.9-slim as backendcore

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        gettext \
        postgresql-client \
        libmagic-dev
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt



FROM backendcore as backenddeploy
RUN useradd -ms /bin/bash pyuser
USER pyuser

COPY --chown=pyuser:pyuser . /app
ENV DJANGO_SETTINGS_MODULE=project.settings.deploy
CMD bash scripts/start_webapi.sh



FROM backendcore as backenddev
COPY requirements-dev.txt /app
RUN pip install -r requirements-dev.txt
USER root

COPY . /app
ENV DJANGO_SETTINGS_MODULE=project.settings.dev
RUN bash scripts/code_scanning.sh
CMD bash scripts/start_webapi.sh
