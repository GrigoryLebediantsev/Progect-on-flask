from app.models.users import User
from app.models.questions import Question
from app.adapter.in_memory import InMemoryDatabase
from app.services.expression_servise import ExpressionServise
from app.adapter.history import UserHistory


class AnswerChecker:
    @staticmethod
    def check_expression_answer(
        expression_id: int, user_id: int, user_answer: int
    ) -> tuple[str, int]:

        expression = InMemoryDatabase.get_expression(expression_id)
        user = InMemoryDatabase.get_user(user_id)

        result = expression.check_answer(user_answer)

        if result == "correct":
            user.increase_score(expression.reward)
            reward = expression.reward
        else:
            reward = 0

        ExpressionServise.add_expression_answer_to_history(
            expression_id, user_id, user_answer, result, reward #Добавить баллы
        )

        return result, reward

    @staticmethod
    def check_question_answer(question: Question, user: User, user_answer: str) -> dict:
        if question.answer == user_answer:
            user.increase_score(question.reward)
            return {"result": "correct", "reward": question.reward}
        else:
            return {"result": "wrong", "reward": 0}
