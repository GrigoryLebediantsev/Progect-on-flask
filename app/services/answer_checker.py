from app.adapter import InMemoryDatabase
from app.services import ExpressionCreateService
from app.services.question_in_history import QuestionInMemory


class AnswerChecker:
    @staticmethod
    def check_expression_answer(user_id: int, user_answer: int, expression_id: int) -> tuple[str, int]:

        expression = InMemoryDatabase.get_expression(expression_id)
        user = InMemoryDatabase.get_user(user_id)

        if expression.check_answer(user_answer):
            user.increase_score(expression.reward)
            reward = expression.reward
            result = "correct"
        else:
            reward = 0
            result = "wrong"

        ExpressionCreateService.add_expression_answer_to_history(
            expression,
            user,
            user_answer,
            result,
            reward,
        )

        return result, reward

    @staticmethod
    def check_question_answer(user_id: int, user_answer: int | str, question_id: int):

        question = InMemoryDatabase.get_question(question_id)
        user = InMemoryDatabase.get_user(user_id)



        if question.check_answer(user_answer):
            user.increase_score(question.reward)
            reward = question.reward
            result = "correct"
        else:
            reward = 0
            result = "wrong"

        QuestionInMemory.add_question_answer_to_history(
            question, user_id, user_answer, result, reward
        )

        return result, reward
