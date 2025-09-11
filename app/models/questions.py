from typing import Protocol, Optional, TypeVar
from app.dto import QuestionType

T = TypeVar("T", str, int)


class QuestionInterface[T](Protocol):
    title: str
    description: str
    reward: int
    type: QuestionType
    id: Optional[int]
    answer: T

    def to_dict(self) -> dict: ...

    def check_answer(self, user_answer: T) -> bool: ...


class OneAnswerQuestion(QuestionInterface[str]):
    def __init__(
        self,
        title: str,
        description: str,
        answer: str,
        reward: int = 1,
        id: Optional[int] = None,
    ):
        self.title = title
        self.description = description
        self.reward = reward
        self.type = QuestionType.ONE_ANSWER
        self.id = id
        self.answer = answer

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "answer": self.answer,
        }

    def check_answer(self, user_answer: str) -> bool:
        return user_answer == self.answer

class MultipleChoiceQuestion(QuestionInterface[int]):
    def __init__(
        self,
        title: str,
        description: str,
        answer: int,
        choices: list[str],
        reward: int = 1,
        id: Optional[int] = None,
    ):
        self.title = title
        self.description = description
        self.reward = reward
        self.type = QuestionType.MULTIPLE_CHOICE
        self.choices = choices
        self.id = id
        self.answer = answer

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "choices": self.choices,
            "answer": self.answer,
        }

    def check_answer(self, user_answer: int) -> bool:
        return user_answer == self.answer
