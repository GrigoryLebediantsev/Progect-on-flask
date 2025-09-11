from app import dto
from app.adapter import InMemoryDatabase
from app.services import UserCreateService, LeaderboardGenerator

from app import app

from pydantic import ValidationError
from flask import request, Response
from http import HTTPStatus
from json import dumps


@app.post("/users/create")
def user_create() -> Response:
    data = request.get_json()
    try:
        user_input = dto.GenerateUserInput(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            email=data["email"],
            score=data["score"],
        )
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    user= UserCreateService.create_user(**user_input.model_dump())

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
        return Response("Пользователя с таким id не существует", status=HTTPStatus.NOT_FOUND)
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
        user_history = InMemoryDatabase.get_user_history(user_id)
    except KeyError:
        return Response(
            "Пользователя с таким id не существует", status=HTTPStatus.NOT_FOUND
        )

    return Response(
        dumps(user_history),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/users/leaderboard")
def get_user_leaderboard() -> Response:
    data = request.get_json()
    try:
        leaderboard_input = dto.GenerateLeaderboardInput(type=data["type"])
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    response_data = LeaderboardGenerator.create_leaderboard(leaderboard_input.type)

    if leaderboard_input.type == "table":
        return Response(
            dumps(response_data), status=HTTPStatus.OK, content_type="application/json"
        )
    else:
        return Response(response_data, status=HTTPStatus.OK, content_type="image/png")
