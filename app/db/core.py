import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from regions.models import DBRegion
from provinces.models import DBProvince
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()