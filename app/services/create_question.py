from app.models import OneAnswerQuestion, MultipleChoiceQuestion, QuestionInterface
from app.dto import QuestionUnion, QuestionType
from app.adapter import InMemoryDatabase


class QuestionCreateService:

    @staticmethod
    def create_question(question_input: QuestionUnion) -> QuestionInterface:

        if question_input.type == QuestionType.ONE_ANSWER:
            question = OneAnswerQuestion(
                title=question_input.title,
                description=question_input.description,
                answer=question_input.answer,
            )
        else:
            question = MultipleChoiceQuestion(
                title=question_input.title,
                description=question_input.description,
                answer=question_input.answer,
                choices=question_input.choices,
            )

        InMemoryDatabase.add_question(question=question)

        return question


