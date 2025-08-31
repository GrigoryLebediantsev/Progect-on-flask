from app.models.questions import Question, OneAnswer, MultipyChoice
from app.dto.questions import GenerateQuestionInput
from app.adapter.in_memory import InMemoryDatabase
from app.adapter.history import UserHistory


class QuestionServise:

    @staticmethod
    def create_question(question_input: GenerateQuestionInput) -> Question:

        if question_input.type == "ONE-ANSWER":
            question = OneAnswer(title=question_input.title, description=question_input.description, answer=question_input.answer)
        else:
            question = MultipyChoice(title=question_input.title, description=question_input.description,
                                 answer=question_input.answer, choices=question_input.choices)

        InMemoryDatabase.add_question(question=question)

        return question

    @classmethod
    def add_question_answer_to_history(cls, question: Question, user_id: int, user_answer: int,
                                  result: str, reward: int) -> None:

        if question.type == "ONE-ANSWER":
            data_to_history = cls.create_one_answer_data(question, user_answer, result, reward)
        else:
            data_to_history = cls.create_multiple_choice_data(question, user_answer, result, reward)

        UserHistory.add_to_user_history(user_id, data_to_history)

    @staticmethod
    def create_one_answer_data(question: Question, user_answer: int,
                                  result: str, reward: int) -> dict:

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
    def create_multiple_choice_data(question: Question, user_answer: int,
                                  result: str, reward: int) -> dict:
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


