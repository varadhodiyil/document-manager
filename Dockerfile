# syntax=docker/dockerfile:1
ARG RUNNING_ENV=local
ARG VIRTUAL_ENV="/opt/venv"

FROM  python:3.11.7-slim as builder_base
RUN addgroup appgroup && useradd -ms /bin/bash appuser
RUN apt-get update && apt-get install -y \
    bash pkg-config python3-dev default-libmysqlclient-dev  build-essential \
    && pip install -U pip 


FROM builder_base as builder_local
COPY requirements/ ./requirements


ARG VIRTUAL_ENV
RUN python -m venv $VIRTUAL_ENV
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
RUN pip install -r ./requirements/local.txt


FROM builder_local as builder_prod

ARG VIRTUAL_ENV
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
RUN pip install -r ./requirements/production.txt


FROM builder_base AS base




FROM base AS base_prod
WORKDIR /app


ARG VIRTUAL_ENV
COPY --from=builder_prod --chown=appuser:appgroup ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=appuser:appgroup . /app

FROM builder_local AS base_local
WORKDIR /app
ARG VIRTUAL_ENV
COPY --from=builder_local --chown=appuser:appgroup  ${VIRTUAL_ENV} ${VIRTUAL_ENV}


FROM base_${RUNNING_ENV} AS final_stage
USER appuser

ARG VIRTUAL_ENV
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"