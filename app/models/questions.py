from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar("T", str, int)


class Question(ABC, Generic[T]):
    def __init__(self, title: str, description: str, reward: int, type: str):
        self.title = title
        self.description = description
        self.reward = reward
        self.type = type
        self.id: Optional[int] = None
        self.choices: Optional[list[str]] = None

    @property
    @abstractmethod
    def answer(self) -> T:
        ...

    @abstractmethod
    def to_dict(self, question_id: int) -> dict: ...

    @abstractmethod
    def check_answer(self, user_answer: T) -> str:
        ...

    def add_id_from_memory(self, id: int) -> None:
        self.id = id


class OneAnswer(Question[str]):
    def __init__(
        self,
        title: str,
        description: str,
        answer: str,
        reward: int = 1,
        type: str = "ONE-ANSWER",
    ):
        super().__init__(title=title, description=description, reward=reward, type=type)
        self._answer = answer

    @property
    def answer(self) -> str:
        return self._answer

    @answer.setter
    def answer(self, value: str) -> None:
        self._answer = value

    def to_dict(self, question_id: int) -> dict:
        return {
            "id": question_id,
            "title": self.title,
            "description": self.description,
            "type": "ONE-ANSWER",
            "answer": self._answer,
        }

    def check_answer(self, user_answer: str) -> str:
        return "correct" if user_answer == self._answer else "wrong"


class MultipyChoice(Question[int]):
    def __init__(
        self,
        title: str,
        description: str,
        choices: list[str],
        answer: int,
        reward: int = 1,
        type: str = "MULTIPLE-CHOICE",
    ):
        super().__init__(title=title, description=description, reward=reward, type=type)
        self._answer = answer
        self.choices = choices

    @property
    def answer(self) -> int:
        return self._answer

    @answer.setter
    def answer(self, value: int) -> None:
        self._answer = value

    def to_dict(self, question_id: int) -> dict:
        return {
            "id": question_id,
            "title": self.title,
            "description": self.description,
            "type": "MULTIPLE-CHOICE",
            "choices": self.choices,
            "answer": self._answer,
        }

    def check_answer(self, user_answer: int) -> str:
        return "correct" if user_answer == self._answer else "wrong"
