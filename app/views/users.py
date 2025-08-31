from pydantic import ValidationError

from app import app
from flask import request, Response
from http import HTTPStatus
from json import dumps
from app.dto.users import GenerateUserInput
from app.adapter.in_memory import InMemoryDatabase
from app.adapter.history import UserHistory
from app.services.user_servise import UserService


@app.post("/users/create")
def user_create() -> Response:
    data = request.get_json()
    try:
        user_input = GenerateUserInput(**data)
    except ValidationError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)
    user = UserService.create_user(user_input)

    return Response(
        dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/users/<int:user_id>/")
def get_user(user_id: int) -> Response:
    try:
        user = InMemoryDatabase.get_user(user_id)
    except KeyError:
        return Response("Нету пользователя с таким id", status=HTTPStatus.NOT_FOUND)
    return Response(
        dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/users/<int:user_id>/history")
def get_history(user_id: int) -> Response:
    try:
        user_history = UserHistory.get_user_history(user_id)
    except KeyError:
        return Response("Не существует пользователя с таким id", status=HTTPStatus.NOT_FOUND)

    return Response(
        dumps(user_history),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

@app.get("/users/leaderboard")
def get_user_leaderboard() -> Response:
    leaderboard_type = request.get_json()["type"]
    try:
        response_data = UserService.create_leaderboard(leaderboard_type)
    except ValueError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)
    if leaderboard_type == "table":
        return Response(dumps(response_data), status=HTTPStatus.OK, content_type="application/json")
    else:
        return Response(response_data, status=HTTPStatus.OK, content_type="image/png")
