from app.application import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os


# DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# DATABASE_URL = "postgresql+psycopg2://admin:secret@host.docker.internal:5432/testdb" #при загрузке в проекте

DATABASE_URL = "postgresql://admin:secret@db:5432/testdb" #при загрузке в проекте



base_engine = create_engine(url=DATABASE_URL)

Session = sessionmaker(bind=base_engine)


class Base(DeclarativeBase):
    pass


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
