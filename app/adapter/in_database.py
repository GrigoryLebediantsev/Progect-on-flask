from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy import JSON, Enum, create_engine, ForeignKey, select
from app.adapter.interface import DatabaseInterface

# from app.adapter.database import Base
import random
from app.dto import QuestionType
from app.models import QuestionInterface, Expression, User
from app.exceptions import (
    UserNotFoundError,
    HistoryNotFoundError,
    ExpressionNotFoundError,
    QuestionNotFoundError,
)


class Base(DeclarativeBase):
    pass


DATABASE_URL = "postgresql://admin:secret@localhost:5432/testdb"

base_engine = create_engine(url=DATABASE_URL)

Session = sessionmaker(bind=base_engine)


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    score: Mapped[int]


class ExpressionOrm(Base):
    __tablename__ = "expressions"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation: Mapped[str]
    values: Mapped[list[str]] = mapped_column(JSON)
    answer: Mapped[str]
    reward: Mapped[int]


class QuestionOrm(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    reward: Mapped[int]
    type: Mapped[QuestionType]
    answer: Mapped[str]

class UserHistoryOrm(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    history_data: Mapped[list] = mapped_column(JSON, nullable=True)

class Database(DatabaseInterface):
    @staticmethod
    def add_user(user: User) -> None:
        with Session() as session:
            user = UserOrm(
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                email=user.email,
                score=user.score,
            )
            session.add(user)
            session.commit()

    @staticmethod
    def get_user(user_id: int) -> User:
        with Session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            user_from_db = session.execute(query).scalar()
            user = User(
                first_name=user_from_db.first_name,
                last_name=user_from_db.last_name,
                phone=user_from_db.phone,
                email=user_from_db.email,
                score=user_from_db.score,
            )
            return user

    @staticmethod
    def get_all_users() -> list[User]:
        with Session() as session:
            query = select(UserOrm)
            response = session.execute(query)
            users = response.all()
            all_users = []
            for user_from_db in users:
                user = User(
                    first_name=user_from_db.first_name,
                    last_name=user_from_db.last_name,
                    phone=user_from_db.phone,
                    email=user_from_db.email,
                    score=user_from_db.score,
                )
                all_users.append(user)
            return all_users

    @staticmethod
    def create_user_history(user_id: int) -> None:
        with Session() as session:
            user_history = UserHistoryOrm(user_id=user_id)
            session.add(user_history)
            session.commit()

    @staticmethod
    def get_user_history(user_id: int) -> dict:
        with Session() as session:
            stmt = select(UserHistoryOrm).where(UserHistoryOrm.user_id == user_id)
            result = session.execute(stmt)
            user_history = result.scalar()
        return {"history": [user_history.history_data]}

    @staticmethod
    def add_to_user_history(user_id: int, data_to_history: dict) -> None:
        with Session() as session:
            query = select(UserHistoryOrm).where(UserHistoryOrm.user_id == user_id)
            result = session.execute(query).scalar()
            result.history_data.append(data_to_history)
            session.commit()

    @staticmethod
    def add_expression(expression: Expression) -> None: ...

    @staticmethod
    def get_expression(expression_id: int) -> Expression: ...

    @staticmethod
    def add_question(question: QuestionInterface) -> None: ...

    @staticmethod
    def get_question(question_id: int) -> QuestionInterface: ...

    @staticmethod
    def get_random_question() -> QuestionInterface: ...
