import random

from app.models import Question
from app.models.expressions import Expression
from app.models.users import User

_USERS = {}
_users_id_counter = 0

_EXPRS: dict = {}
_exprs_id_counter: int = 0

_QUESTS: dict = {}
_quests_id_counter: int = 0


class InMemoryDatabase:

    @staticmethod
    def create_user(user: User) -> int:
        """Сохраняет пользователя. Возвращает ID пользователя."""
        global _users_id_counter, _USERS

        _USERS[_users_id_counter] = user
        _users_id_counter += 1

        return _users_id_counter - 1

    @staticmethod
    def get_user(user_id: int) -> User:
        """Возвращает пользователя по ID."""
        try:
            return _USERS[user_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def create_expression(expression: Expression) -> int:
        """Сохраняет задание. Возвращает ID задания."""
        global _exprs_id_counter, _EXPRS

        _EXPRS[_exprs_id_counter] = expression
        _exprs_id_counter += 1

        return _exprs_id_counter - 1

    @staticmethod
    def get_expression(expression_id: int) -> Expression:
        """Возвращает задание по ID."""
        try:
            return _EXPRS[expression_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def create_question(question: Question) -> int:
        """Сохраняет вопрос. Возвращает ID вопроса."""
        global _quests_id_counter, _QUESTS

        _QUESTS[_quests_id_counter] = question
        _quests_id_counter += 1

        return _quests_id_counter - 1

    @staticmethod
    def get_question(question_id: int) -> Question:
        """Возвращает вопрос по ID."""
        try:
            return _QUESTS[question_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def get_random_quest_id() -> int:
        """Возвращает ID случайного вопроса"""
        random_quest_id = random.randint(0, len(_QUESTS) - 1)
        return random_quest_id

    @staticmethod
    def exression_in_memory(): ...
