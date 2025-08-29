from app import app, models
from flask import request, Response
from http import HTTPStatus
from json import dumps
from app.services.answer_checker import AnswerChecker
from app.adapter.in_memory import InMemoryDatabase
from app.dto.questions import GenerateQuestionInput
from app.adapter.history import UserHistory


@app.post("/questions/create")
def create_question():
    data = request.get_json()

    question_input = GenerateQuestionInput(**data)

    if data["type"] == "ONE-ANSWER":
        question = models.OneAnswer(
            question_input.title, question_input.description, question_input.answer
        )
        question_id = InMemoryDatabase.create_question(question)
        return Response(
            dumps(
                {
                    "id": question_id,
                    "title": question.title,
                    "description": question.description,
                    "type": "ONE-ANSWER",
                    "answer": question.answer,
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    elif data["type"] == "MULTIPLE-CHOICE":
        question = models.MultipyChoice(
            question_input.title,
            question_input.description,
            question_input.choices,
            question_input.answer,
        )
        question_id = InMemoryDatabase.create_question(question)
        return Response(
            dumps(
                {
                    "id": question_id,
                    "title": question.title,
                    "description": question.description,
                    "type": "MULTIPLE-CHOICE",
                    "choices": question.choices,
                    "answer": question.answer,
                }
            ),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        return Response(
            "Нельзя сгенерировать такой тип вопроса", status=HTTPStatus.BAD_REQUEST
        )


@app.get("/questions/random")
def random_quest():
    question_id = InMemoryDatabase.get_random_quest_id()
    question = InMemoryDatabase.get_question(question_id)
    return Response(
        dumps(
            {
                "id": question_id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@app.post("/questions/<int:question_id>/solve")
def solve_quest(question_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]
    user = InMemoryDatabase.get_user(user_id)
    question = InMemoryDatabase.get_question(question_id)
    result = AnswerChecker.check_question_answer(question, user, user_answer)

    data_to_history = {
        "title": question.title,
        "description": question.description,
        "type": question.type,
        "answer": question.answer,
        "user_answer": user_answer,
        "reward": result["reward"],
    }

    UserHistory.add_question_to_history(
        user_id, data_to_history
    )

    return Response(
        dumps(
            {
                "question_id": question_id,
                **result,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
