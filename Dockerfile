FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .
CMD ["poetry", "run", "uvicorn", "messagingservice.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
