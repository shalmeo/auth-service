FROM python:3.11.6-slim as python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:$PATH

FROM python-base AS builder-base

WORKDIR ${PROJECT_PATH:-/app}

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./requirements.txt ./

RUN python -m venv /opt/venv
RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

FROM python-base

WORKDIR ${PROJECT_PATH:-/app}

COPY --from=builder-base /opt/venv /opt/venv
COPY ./diagnosix_auth ./diagnosix_auth