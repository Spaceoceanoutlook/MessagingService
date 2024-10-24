FROM python:3.12
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .
CMD ["poetry", "run", "uvicorn", "messagingservice.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
