from app.models import QuestionInterface, OneAnswerQuestion, MultipleChoiceQuestion
from app.dto import QuestionType
from app.adapter import InMemoryDatabase


class QuestionInMemory:
    @classmethod
    def add_question_answer_to_history(
        cls,
        question: QuestionInterface,
        user_id: int,
        user_answer: int,
        result: str,
        reward: int,
    ) -> None:

        if question.type == QuestionType.ONE_ANSWER:
            data_to_history = cls.create_one_answer_data(
                question, user_answer, result, reward
            )
        else:
            data_to_history = cls.create_multiple_choice_data(
                question, user_answer, result, reward
            )

        InMemoryDatabase.add_to_user_history(user_id, data_to_history)

    @staticmethod
    def create_one_answer_data(
        question: OneAnswerQuestion, user_answer: int, result: str, reward: int
    ) -> dict:

        data = {
            "id": question.id,
            "title": question.title,
            "description": question.description,
            "type": question.type,
            "answer": question.answer,
            "user_answer": user_answer,
            "result": result,
            "reward": reward,
        }
        return data

    @staticmethod
    def create_multiple_choice_data(
        question: MultipleChoiceQuestion, user_answer: int, result: str, reward: int
    ) -> dict:
        data = {
            "id": question.id,
            "title": question.title,
            "description": question.description,
            "type": question.type,
            "choices": question.choices,
            "answer": question.answer,
            "user_answer": user_answer,
            "result": result,
            "reward": reward,
        }
        return data