from app.models.expressions import Expression
from app.dto.expressions import GenerateExpressionInput
from app.adapter.in_memory import InMemoryDatabase
from app.adapter.history import UserHistory


class ExpressionServise:

    @staticmethod
    def create_expression(expression_input: GenerateExpressionInput) -> tuple[Expression, int]:
        expression = Expression(
            expression_input.operation,
            expression_input.values,
            reward=expression_input.reward,
        )
        expression_id = InMemoryDatabase.create_expression(expression=expression)
        return expression, expression_id

    @staticmethod
    def add_expression_answer_to_history(expression_id: int, user_id: int, user_answer: int,
                                  result: str, reward: int) -> None:

        expression = InMemoryDatabase.get_expression(expression_id)

        data_to_history = {
            "id": expression_id,
            "operation": expression.operation,
            "values": expression.values,
            "answer": expression.answer,
            "user_answer": user_answer,
            "result": result,
            "reward": reward,
        }
        UserHistory.add_to_user_history(user_id, data_to_history)

