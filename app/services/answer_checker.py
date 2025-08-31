from app.adapter.in_memory import InMemoryDatabase
from app.services.expression_servise import ExpressionServise
from app.dto.expression_solve import SolveExpressionInput
from app.dto.question_solve import SolveQuestionInput
from app.services.question_servise import QuestionServise


class AnswerChecker:
    @staticmethod
    def check_expression_answer(input_dto: SolveExpressionInput) -> tuple[str, int]:

        expression = InMemoryDatabase.get_expression(input_dto.expression_id)
        user = InMemoryDatabase.get_user(input_dto.user_id)

        result = expression.check_answer(input_dto.user_answer)

        if result == "correct":
            user.increase_score(expression.reward)
            reward = expression.reward
        else:
            reward = 0

        ExpressionServise.add_expression_answer_to_history(
            expression,
            user,
            input_dto.user_answer,
            result,
            reward,
        )

        return result, reward

    @staticmethod
    def check_question_answer(input_dto: SolveQuestionInput):

        question = InMemoryDatabase.get_question(input_dto.question_id)
        user = InMemoryDatabase.get_user(input_dto.user_id)

        result = question.check_answer(input_dto.user_answer)

        if result == "correct":
            user.increase_score(question.reward)
            reward = question.reward
        else:
            reward = 0

        QuestionServise.add_question_answer_to_history(question, input_dto.user_id, input_dto.user_answer, result, reward)

        return result, reward
