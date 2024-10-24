import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DB")
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
