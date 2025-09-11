from pydantic import BaseModel, model_validator
from enum import Enum
from typing import Self, Optional


class QuestionType(Enum):
    ONE_ANSWER = "ONE-ANSWER"
    MULTIPLE_CHOICE = "MULTIPLE-CHOICE"



class GenerateQuestionInput(BaseModel):
    title: str
    description: str
    type: QuestionType

class MultipleChoiceQuestionInput(GenerateQuestionInput):
    choices: Optional[list[str]]
    answer: int

class OneAnswerQuestionInput(GenerateQuestionInput):
    answer: str




