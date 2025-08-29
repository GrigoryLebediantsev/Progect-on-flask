from pydantic import BaseModel, computed_field, model_validator

class GenerateQuestionInput(BaseModel):
    title: str
    description: str
    type: str
    choices: list[str] | None = None
    answer: str | int

    @model_validator(mode="after")
    def check_type(self):
        if self.type == "ONE-ANSWER" and not isinstance(self.answer, str):
            raise ValueError("Для вопроса с одним вариантом ответа ответ должен быть в строковом виде")
        elif self.type == "MULTIPLE-CHOICE" and not isinstance(self.answer, int):
            raise ValueError("Для вопроса с множественными вариантами ответа ответ должен иметь целочисленное значение")




