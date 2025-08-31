from pydantic import BaseModel, field_validator
from app.adapter.in_memory import InMemoryDatabase


class SolveQuestionInput(BaseModel):
    user_id: int
    user_answer: int | str
    question_id: int

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: int) -> int:
        if not InMemoryDatabase.user_in_memory(value):
            raise ValueError("Не существует пользователя с таким id")
        return value

    @field_validator("question_id")
    @classmethod
    def validate_question_id(cls, value: int) -> int:
        if not InMemoryDatabase.expression_in_memory(value):
            raise ValueError("Не существует выражения с таким id")
        return value

