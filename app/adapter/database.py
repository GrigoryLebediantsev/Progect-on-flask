from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass

DATABASE_URL = "postgresql://admin:secret@localhost:5432/testdb"

base_engine = create_engine(url=DATABASE_URL)

Session = sessionmaker(bind=base_engine)