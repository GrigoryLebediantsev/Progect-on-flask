from pydantic import BaseModel, Field
from typing import Annotated

class SolveExpressionInput(BaseModel):
    user_id: Annotated[int, Field(ge=0)]
    user_answer: int
    expression_id: Annotated[int, Field(ge=0)]
