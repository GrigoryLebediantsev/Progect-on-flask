from app.adapter.database.tables import UserOrm, ExpressionOrm, QuestionOrm, UserHistoryOrm
from app.main import Session
from sqlalchemy import select
from sqlalchemy.sql import func
from app.adapter.interface import DatabaseInterface
from app.dto import QuestionType
from app.models import (
    QuestionInterface,
    Expression,
    User,
    OneAnswerQuestion,
    MultipleChoiceQuestion,
)

from app.exceptions import (
    UserNotFoundError,
    HistoryNotFoundError,
    ExpressionNotFoundError,
    QuestionNotFoundError,
)


class Database(DatabaseInterface):
    @staticmethod
    def add_user(user: User) -> None:
        with Session() as session:
            user_orm = UserOrm(
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                email=user.email,
                score=user.score,
            )
            session.add(user_orm)
            session.commit()
            session.refresh(user_orm)
            user.id = user_orm.id

    @staticmethod
    def get_user(user_id: int) -> User:
        with Session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            user_from_db = session.execute(query).scalar_one_or_none()
            if user_from_db is None:
                raise UserNotFoundError(f"Пользователь {user_id} не найден")
            user = User(
                id=user_from_db.id,
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
            users = response.scalars().all()
            if users is None:
                raise UserNotFoundError(
                    "В базе данных не обнаружено ни одного пользователя"
                )
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
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                raise HistoryNotFoundError(f"История для пользователя {user_id} не найдена")
        return {"history": result.history_data}

    @staticmethod
    def add_to_user_history(user_id: int, data_to_history: dict) -> None:
        with Session() as session:
            query = select(UserHistoryOrm).where(UserHistoryOrm.user_id == user_id)
            result = session.execute(query).scalar_one_or_none()
            if result is None:
                raise HistoryNotFoundError(f"История для пользователя {user_id} не найдена")
            result.history_data.append(data_to_history)
            session.commit()

    @staticmethod
    def add_expression(expression: Expression) -> None:
        with Session() as session:
            expression_orm = ExpressionOrm(
                operation=expression.operation,
                values=expression.values,
                answer=expression.answer,
                reward=expression.reward,
            )
            session.add(expression_orm)
            session.commit()
            session.refresh(expression_orm)
            expression.id = expression_orm.id

    @staticmethod
    def get_expression(expression_id: int) -> Expression:
        with Session() as session:
            query = select(ExpressionOrm).where(ExpressionOrm.id == expression_id)
            expression_from_db = session.execute(query).scalar_one_or_none()
            if expression_from_db is None:
                raise ExpressionNotFoundError(f"Выражение {expression_id} не найдено")
            expression = Expression(
                operation=expression_from_db.operation,
                values=expression_from_db.values,
                reward=expression_from_db.reward,
            )
            return expression

    @staticmethod
    def add_question(question: QuestionInterface) -> None:
        with Session() as session:
            question_orm = QuestionOrm(
                description=question.description,
                reward=question.reward,
                type=question.type,
                answer=question.answer,
            )
            session.add(question_orm)
            session.commit()
            session.refresh(question_orm)
            question.id = question_orm.id

    @staticmethod
    def get_question(question_id: int) -> QuestionInterface:
        with Session() as session:
            query = select(QuestionOrm).where(QuestionOrm.id == question_id)
            question_from_db = session.execute(query).scalar_one_or_none()
            if question_from_db is None:
                raise QuestionNotFoundError(f"Вопрос {question_id} не найден")
            if question_from_db.type == QuestionType.ONE_ANSWER:
                question = OneAnswerQuestion(
                    title=question_from_db.title,
                    description=question_from_db.description,
                    answer=question_from_db.answer,
                )
            else:
                question = MultipleChoiceQuestion(
                    title=question_from_db.title,
                    description=question_from_db.description,
                    answer=question_from_db.answer,
                    choices=question_from_db.choices,
                )
            return question

    @staticmethod
    def get_random_question() -> QuestionInterface:
        with Session() as session:
            query = select(QuestionOrm).where(func.random()).limit(1)
            question_from_db = session.execute(query).scalar_one_or_none()
            if question_from_db is None:
                raise QuestionNotFoundError(f"Ошибка генерации случайного вопроса")
            if question_from_db.type == QuestionType.ONE_ANSWER:
                question = OneAnswerQuestion(
                    title=question_from_db.title,
                    description=question_from_db.description,
                    answer=question_from_db.answer,
                )
            else:
                question = MultipleChoiceQuestion(
                    title=question_from_db.title,
                    description=question_from_db.description,
                    answer=question_from_db.answer,
                    choices=question_from_db.choices,
                )
            return question

