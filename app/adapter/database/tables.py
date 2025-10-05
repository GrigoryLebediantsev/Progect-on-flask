from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import JSON, ForeignKey
from app.dto import QuestionType
from app.main import base_engine, Base

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
    values: Mapped[list[int]] = mapped_column(JSON)
    answer: Mapped[str]
    reward: Mapped[int]


class QuestionOrm(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    reward: Mapped[int]
    type: Mapped[QuestionType]
    answer: Mapped[str]
    choices: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), nullable=True)
    title: Mapped[str]


class UserHistoryOrm(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    history_data: Mapped[list] = mapped_column(
        MutableList.as_mutable(JSON), default=list
    )

Base.metadata.drop_all(base_engine)

Base.metadata.create_all(base_engine)