import random
from typing import Self, Literal
from pydantic import BaseModel, model_validator, computed_field, Field


class GenerateExpressionInput(BaseModel):
    count_nums: int = Field(ge=0)
    operation: Literal["+", "-", "*", "/", "**", "random"]
    min: int
    max: int

    @model_validator(mode="after")
    def normalize_operation(self) -> Self:
        if not self.operation == "random":
            return self
        if self.count_nums > 2:
            self.operation = random.choice(["+", "*", "**"])

        else:
            self.operation = random.choice(["+", "*", "**", "-", "/"])
        return self

    @model_validator(mode="after")
    def check_operation(self) -> Self:
        if self.count_nums > 2 and self.operation not in {"+", "*", "**"}:
            raise ValueError(
                "Более двух операций поддерживаются только для умножения, возведения в степень и сложения"
            )
        return self

    @model_validator(mode="after")
    def check_count_nums(self) -> Self:
        if self.operation in {"-", "/"}:
            if self.count_nums > 2:
                raise ValueError("Для этих операций недоступное количество значений")
        return self

    @model_validator(mode="after")
    def check_min_max(self) -> Self:
        if self.min > self.max:
            raise ValueError("Минимальное значение не должно превышать максимальное")
        return self

    @computed_field(return_type=int)
    def reward(self) -> int:
        return self.count_nums - 1 if self.count_nums > 2 else 1

    @computed_field(return_type=list[int])
    def values(self) -> list:
        return [random.randint(self.min, self.max) for _ in range(self.count_nums)]
