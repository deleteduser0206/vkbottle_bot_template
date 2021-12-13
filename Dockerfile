FROM python:3.7.2-slim as base

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY pyproject.toml ./

RUN python -m pip install pip wheel setuptools --upgrade

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY src ./src
COPY config.yml docker-entrypoint.sh ./

RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]
