from app.services import AnswerChecker, QuestionCreateService
from app.adapter import InMemoryDatabase
from app.exceptions import QuestionNotFoundError, UserNotFoundError
from app import dto

from app.application import app

from pydantic import ValidationError
from flask import request, Response
from http import HTTPStatus
from json import dumps

from app.deps import get_storage

Storage = get_storage()


@app.post("/questions/create")
def create_question():
    data = request.get_json()

    try:
        question_input = dto.QuestionUnion(
            title=data["title"],
            description=data["description"],
            type=data["type"],
            choices=data["choices"],
            answer=data["answer"],
        )
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    question = QuestionCreateService.create_question(question_input)
    question_output = question.to_dict()

    return Response(
        dumps(question_output), status=HTTPStatus.OK, content_type="application/json"
    )


@app.get("/questions/random")
def random_quest():
    try:
        question = Storage.get_random_question()
    except QuestionNotFoundError:
        return Response(
            "Нет ни одного вопроса в базе данных",
            status=HTTPStatus.NOT_FOUND,
        )

    return Response(
        dumps(
            {
                "id": question.id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@app.post("/questions/<int:question_id>/solve")
def solve_quest(question_id):
    data = request.get_json()

    try:
        input_dto = dto.SolveQuestionInput(
            user_id=data["user_id"],
            user_answer=data["user_answer"],
            question_id=question_id,
        )
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    try:
        result, reward = AnswerChecker.check_question_answer(
            input_dto.user_id, input_dto.user_answer, input_dto.question_id
        )
    except QuestionNotFoundError:
        return Response(
            "Вопроса с таким id не существует в базе", status=HTTPStatus.NOT_FOUND
        )
    except UserNotFoundError:
        return Response(
            "Пользователя с таким id не существует в базе", status=HTTPStatus.NOT_FOUND
        )

    return Response(
        dumps(
            {
                "question_id": question_id,
                "result": result,
                "reward": reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
