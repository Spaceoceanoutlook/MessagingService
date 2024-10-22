import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    return f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"
