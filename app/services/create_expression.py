from app.models import Expression
from app.adapter import InMemoryDatabase


class ExpressionCreateService:

    @staticmethod
    def create_expression(operation: str, values: list[int], reward: int) -> Expression:
        expression = Expression(
            operation,
            values,
            reward=reward,
        )
        InMemoryDatabase.add_expression(expression=expression)
        return expression

    @classmethod
    def add_expression_answer_to_history(cls, expression, user, user_answer, result, reward):
        pass
