from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine
from app.config import settings


def get_url() -> str:
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    hostname = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    db = settings.POSTGRES_DB

    return f'postgresql://{user}:{password}@{hostname}:{port}/{db}'


SQLALCHEMY_DATABASE_URL = get_url()
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:new_pass@localhost:5432/test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()
session = Session(engine)
