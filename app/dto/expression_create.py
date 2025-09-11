import random
from typing import Self, Literal,Annotated
from pydantic import BaseModel, model_validator, computed_field, Field


class GenerateExpressionInput(BaseModel):
    count_nums: Annotated[int, Field(ge=2)]
    operation: Literal["+", "-", "*", "/", "**", "random"]
    min: int
    max: int
    _values: list[int]

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self._normalize_operation()
        self._check_count_nums()
        self._check_min_max()
        self._generate_values()
        return Self

    @computed_field
    def reward(self) -> int:
        return self.count_nums - 1 if self.count_nums > 2 else 1

    @computed_field
    def values(self) -> list[int]:
        return self._values

    def _normalize_operation(self) -> None:
        if self.operation == "random":
            if self.count_nums > 2:
                self.operation = random.choice(["+", "*", "**"])
            else:
                self.operation = random.choice(["+", "*", "**", "-", "/"])

    def _check_count_nums(self) -> None:
        if self.operation in {"-", "/"}:
            if self.count_nums > 2:
                raise ValueError("Для этих операций недоступное количество значений")

    def _check_min_max(self) -> None:
        if self.min > self.max:
            raise ValueError("Минимальное значение не должно превышать максимальное")

    def _generate_values(self) -> None:
        self._values = [random.randint(self.min, self.max) for _ in range(self.count_nums)]
