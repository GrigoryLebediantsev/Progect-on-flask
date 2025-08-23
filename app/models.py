from abc import ABC, abstractmethod
import re
import random


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):

        if not (
            isinstance(id, int)
            and isinstance(first_name, str)
            and isinstance(last_name, str)
            and isinstance(phone, str)
            and isinstance(email, str)
            and isinstance(score, int)
        ):
            raise ValueError

        if not self.validate_email(email) or not self.validate_phone(phone):
            raise ValueError

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def validate_email(email):
        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return True if valid else False

    @staticmethod
    def validate_phone(phone):
        valid = re.match(r"^\+7\d{10}$", phone)
        return True if valid else False

    def increase_score(self, amount):
        self.score += amount

    def __repr__(self):
        return f"{self.id}) {self.first_name} {self.last_name}"


class Expression:
    OPERATIONS = ["+", "*", "-", "//", "**"]
    def __init__(self, id, operation, *values, reward=None):

        if reward is None:
            reward = len(values) - 1

        if not (
            isinstance(id, int)
            and isinstance(operation, str)
            and isinstance(values, tuple)
            and isinstance(reward, int)
        ):
            raise ValueError

        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        self.reward = reward

    def __evaluate(self):
        return eval(self.to_str)

    @property
    def to_str(self):
        str_values = list(map(str, self.values))
        expr_str = f" {self.operation} ".join(str_values)
        return expr_str

    def __repr__(self):
        return f"{self.id}) {self.to_str} = {self.answer}"

    @staticmethod
    def choose_operation(operation: str) -> str:
        """Возвращает конкретную операцию для Expression"""
        if operation == "random":
            operation = random.choice(["+", "*", "-", "//", "**"])
        if operation not in Expression.OPERATIONS:
            raise ValueError(f"Недопустимая операция: {operation}")
        return operation

    @staticmethod
    def validate_expression_params(count_nums: int, operation: str) -> bool:
        """
        Проверяет, допустимо ли количество чисел для данной операции.
        Для операций +, *, ** можно больше 2 чисел.
        Для остальных только 2 числа.
        """
        if count_nums <= 1:
            return False
        if count_nums > 2 and operation not in {"+", "*", "**"}:
            return False
        return True

    def check_answer(self, user_answer, user):
        """
        Проверяет ответ пользователя и увеличивает его score при верном ответе.
        Возвращает "correct" или "wrong".
        """
        if user_answer == self.answer:
            user.increase_score(self.reward)
            return "correct"
        return "wrong"

class Question(ABC):
    def __init__(self, id: int, title: str, description: str, reward=None):
        self.id = id
        self.description = description
        self.title = title
        if reward is None:
            reward = 1
        self.reward = reward

    @property
    @abstractmethod
    def answer(self):
        pass


class OneAnswer(Question):
    def __init__(self, id: int, title: str, description: str, answer: str, reward=None):
        super().__init__(id, title, description, reward)
        self._answer = answer

    @property
    def answer(self) -> str:
        return self._answer

    @answer.setter
    def answer(self, value):
        self._answer = value

    @staticmethod
    def is_valid(answer) -> bool:
        return isinstance(answer, str)

    def __repr__(self):
        return f"{self.id}) {self.title}"


class MultipyChoice(Question):
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        choices: list,
        answer: int,
        reward=None,
    ):
        super().__init__(id, title, description, reward)
        self._answer = answer
        self.choices = choices

    @property
    def answer(self) -> int:
        return self._answer

    @answer.setter
    def answer(self, value):
        self._answer = value

    @staticmethod
    def is_valid(answer, choices) -> bool:
        if not isinstance(answer, int) or answer < 0 or answer > len(choices):
            return False
        return True

    def __repr__(self):
        return f"{self.id}) {self.title}"
