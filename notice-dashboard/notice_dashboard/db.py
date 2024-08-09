import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from models import Base

db_connection_url = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)
engine = create_engine(db_connection_url)
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)


def get_db_session() -> Session:
    return scoped_session(session_factory)
