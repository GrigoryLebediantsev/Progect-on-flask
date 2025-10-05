import random
from app.models import QuestionInterface, Expression, User
from app.exceptions import (
    UserNotFoundError,
    HistoryNotFoundError,
    ExpressionNotFoundError,
    QuestionNotFoundError,
)

_USERS = {}
_users_id_counter = 1

_HISTORY_ALL_USERS: dict[int, dict] = {}

_EXPRS: dict = {}
_exprs_id_counter: int = 1

_QUESTS: dict = {}
_quests_id_counter: int = 1


class InMemoryDatabase:

    @staticmethod
    def add_user(user: User) -> None:
        global _users_id_counter, _USERS
        _USERS[_users_id_counter] = user
        user.id = _users_id_counter
        _users_id_counter += 1

    @staticmethod
    def get_user(user_id: int) -> User:
        if user_id not in _USERS:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")
        return _USERS[user_id]

    @staticmethod
    def get_all_users() -> list[User]:
        if not _USERS:
            raise UserNotFoundError(
                "В базе данных не обнаружено ни одного пользователя"
            )
        return [_USERS[user_id] for user_id in _USERS]

    @staticmethod
    def create_user_history(user_id: int) -> None:
        _HISTORY_ALL_USERS[user_id] = {"history": []}

    @staticmethod
    def get_user_history(user_id: int) -> dict:
        if user_id not in _HISTORY_ALL_USERS:
            raise HistoryNotFoundError(f"История для пользователя {user_id} не найдена")
        return _HISTORY_ALL_USERS[user_id]

    @staticmethod
    def add_to_user_history(user_id: int, data_to_history: dict) -> None:
        if user_id not in _HISTORY_ALL_USERS:
            raise HistoryNotFoundError(f"История для пользователя {user_id} не найдена")
        _HISTORY_ALL_USERS[user_id]["history"].append(data_to_history)

    @staticmethod
    def add_expression(expression: Expression) -> None:
        global _exprs_id_counter, _EXPRS

        _EXPRS[_exprs_id_counter] = expression
        expression.id = _exprs_id_counter
        _exprs_id_counter += 1

    @staticmethod
    def get_expression(expression_id: int) -> Expression:
        if not expression_id in _EXPRS:
            raise ExpressionNotFoundError(f"Выражение {expression_id} не найдено")
        return _EXPRS[expression_id]

    @staticmethod
    def add_question(question: QuestionInterface) -> None:
        global _quests_id_counter, _QUESTS

        _QUESTS[_quests_id_counter] = question
        question.id = _quests_id_counter
        _quests_id_counter += 1

    @staticmethod
    def get_question(question_id: int) -> QuestionInterface:
        if not question_id in _QUESTS:
            raise QuestionNotFoundError(f"Вопрос {question_id} не найден")
        return _QUESTS[question_id]

    @staticmethod
    def get_random_question() -> QuestionInterface:
        if len(_QUESTS) == 0:
            raise QuestionNotFoundError("В базе данных не обнаружено ни одного вопроса")
        random_quest_id = random.randint(0, len(_QUESTS) - 1)
        random_question = InMemoryDatabase.get_question(random_quest_id)
        return random_question