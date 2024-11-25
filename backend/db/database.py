from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from backend.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

DbSession = Session(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
