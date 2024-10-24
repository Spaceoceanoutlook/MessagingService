from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_config import get_database_url

SQLALCHEMY_DATABASE_URL = get_database_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

