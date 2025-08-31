from app.models import Expression, User
from app.dto.expressions import GenerateExpressionInput
from app.adapter import InMemoryDatabase, UserHistory


class ExpressionServise:

    @staticmethod
    def create_expression(expression_input: GenerateExpressionInput) -> Expression:
        expression = Expression(
            expression_input.operation,
            expression_input.values,
            reward=expression_input.reward,
        )
        InMemoryDatabase.add_expression(expression=expression)
        return expression

    @staticmethod
    def add_expression_answer_to_history(
        expression: Expression, user: User, user_answer: int, result: str, reward: int
    ) -> None:

        data_to_history = {
            "id": expression.id,
            "operation": expression.operation,
            "values": expression.values,
            "answer": expression.answer,
            "user_answer": user_answer,
            "result": result,
            "reward": reward,
        }
        UserHistory.add_to_user_history(user.id, data_to_history)
