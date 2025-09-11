from pydantic import BaseModel, Field
from typing import Annotated


class SolveQuestionInput(BaseModel):
    user_id: Annotated[int, Field(ge=0)]
    user_answer: int | str
    question_id: Annotated[int, Field(ge=0)]



