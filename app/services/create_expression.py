from app.models import Expression, User
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
