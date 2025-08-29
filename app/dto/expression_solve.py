from pydantic import BaseModel, field_validator
from typing import Self
from app.adapter.in_memory import InMemoryDatabase


class SolveExpressionInput(BaseModel):
    user_id: int
    user_answer: int
    expression_id: int

    @field_validator("user_id")
    def validate_user_id(self) -> Self:
        try:
            user = InMemoryDatabase.get_user(self.user_id)   # todo Хотелось бы сделать валидацию без создания юзера
        except KeyError:
            raise ValueError("Не существует пользователя с таким id")
        return self

    @field_validator("expression_id")
    def validate_user_id(self) -> Self:
        try:
            expression = InMemoryDatabase.get_expression(self.expression_id)  # todo Хотелось бы сделать валидацию без создания выражения
        except KeyError:
            raise ValueError("Не существует выражения с таким id")
        return self