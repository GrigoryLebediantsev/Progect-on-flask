from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Annotated, Self


class GenerateUserInput(BaseModel):
    first_name: str
    last_name: str
    phone: Annotated[str, Field(pattern=r"^\+7\d{10}$")]
    email: EmailStr
    score: int = 0

    @model_validator(mode="after")
    def check_name(self) -> Self:
        if (
            self.first_name[0].upper() != self.first_name[0]
            or self.last_name[0].upper() != self.last_name[0]
        ):
            raise ValueError("Имя и отчество должны начинаться с заглавной буквы")
        return self


