from pydantic import BaseModel, field_validator
from app.adapter import InMemoryDatabase

class SolveExpressionInput(BaseModel):
    user_id: int
    user_answer: int
    expression_id: int

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: int) -> int:
        if value < 0 or not InMemoryDatabase.user_in_memory(value):
            raise ValueError("Не существует пользователя с таким id")
        return value

    @field_validator("expression_id")
    @classmethod
    def validate_expression_id(cls, value: int) -> int:
        if value < 0 or not InMemoryDatabase.expression_in_memory(value):
            raise ValueError("Не существует выражения с таким id")
        return value
