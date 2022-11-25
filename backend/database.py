from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

database_name = settings.database_name
username = settings.database_username
password = settings.database_password
port = settings.database_port
hostname = settings.database_hostname


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{username}:{password}@{hostname}/{database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency
    Imported by the router files
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
