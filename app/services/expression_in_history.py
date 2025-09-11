from app.adapter import InMemoryDatabase
from app.models import Expression, User

class ExpressionInHistory:
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
        InMemoryDatabase.add_to_user_history(user.id, data_to_history)