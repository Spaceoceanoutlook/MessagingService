FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apk update && apk add --no-cache \
    wget \
    gcc \
    musl-dev \
    postgresql-dev \
    netcat-openbsd \
    openssl \
    bash \
    && pip install poetry
COPY pyproject.toml poetry.lock ./
RUN wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh
RUN poetry install
COPY . /app
RUN mkdir certs && \
    openssl genrsa -out certs/jwt-private.pem 2048 && \
    openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
CMD ["poetry", "run", "uvicorn", "messagingservice.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
