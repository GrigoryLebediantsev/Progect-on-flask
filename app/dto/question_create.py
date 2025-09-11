from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field
from enum import Enum

class QuestionType(str, Enum):
    ONE_ANSWER = "ONE-ANSWER"
    MULTIPLE_CHOICE = "MULTIPLE-CHOICE"


class GenerateQuestionInput(BaseModel):
    title: str
    description: str
    type: QuestionType


class MultipleChoiceQuestionInput(GenerateQuestionInput):
    type: Literal[QuestionType.MULTIPLE_CHOICE]
    choices: list[str]
    answer: int


class OneAnswerQuestionInput(GenerateQuestionInput):
    type: Literal[QuestionType.ONE_ANSWER]
    answer: str


QuestionUnion = Annotated[
    Union[OneAnswerQuestionInput, MultipleChoiceQuestionInput],
    Field(discriminator="type")
]
