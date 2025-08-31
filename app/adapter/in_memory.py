import random
from app.models import Question, Expression, User

_USERS = {}
_users_id_counter = 0

_EXPRS: dict = {}
_exprs_id_counter: int = 0

_QUESTS: dict = {}
_quests_id_counter: int = 0


class InMemoryDatabase:

    @staticmethod
    def add_user(user: User) -> None:
        """Сохраняет пользователя. Возвращает ID пользователя."""
        global _users_id_counter, _USERS
        _USERS[_users_id_counter] = user
        user.add_id_from_memory(_users_id_counter)
        _users_id_counter += 1

    @staticmethod
    def get_user(user_id: int) -> User:
        """Возвращает пользователя по ID."""
        try:
            return _USERS[user_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def get_all_users() -> list:
        return [_USERS[user_id] for user_id in _USERS]

    @staticmethod
    def user_in_memory(user_id):
        try:
            InMemoryDatabase.get_user(user_id)
        except KeyError:
            return False
        return True

    @staticmethod
    def add_expression(expression: Expression) -> None:
        """Сохраняет задание. Возвращает ID задания."""
        global _exprs_id_counter, _EXPRS

        _EXPRS[_exprs_id_counter] = expression
        expression.add_id_from_memory(_exprs_id_counter)
        _exprs_id_counter += 1

    @staticmethod
    def get_expression(expression_id: int) -> Expression:
        """Возвращает задание по ID."""
        try:
            return _EXPRS[expression_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def expression_in_memory(expression_id: int) -> bool:
        try:
            InMemoryDatabase.get_expression(expression_id)
        except KeyError:
            return False
        return True

    @staticmethod
    def add_question(question: Question) -> None:
        """Сохраняет вопрос. Возвращает ID вопроса."""
        global _quests_id_counter, _QUESTS

        _QUESTS[_quests_id_counter] = question
        question.add_id_from_memory(_quests_id_counter)
        _quests_id_counter += 1

    @staticmethod
    def get_question(question_id: int) -> Question:
        """Возвращает вопрос по ID."""
        try:
            return _QUESTS[question_id]
        except IndexError:
            raise ValueError("Неверный ID")

    @staticmethod
    def question_in_memory(question_id: int) -> bool:
        try:
            InMemoryDatabase.get_question(question_id)
        except KeyError:
            return False
        return True

    @staticmethod
    def get_random_quest_id() -> int:
        """Возвращает ID случайного вопроса"""
        random_quest_id = random.randint(0, len(_QUESTS) - 1)
        return random_quest_id

