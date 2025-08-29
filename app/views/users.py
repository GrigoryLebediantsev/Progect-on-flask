from app.models import User
from app import app
from flask import request, Response
from http import HTTPStatus
from json import dumps
from app.dto.users import GenerateUserInput
from app.adapter.in_memory import InMemoryDatabase
from app.adapter.history import UserHistory


@app.post("/user/create")
def user_create() -> Response:
    data = request.get_json()

    user_input = GenerateUserInput(**data)
    user = User(
        first_name=user_input.first_name,
        last_name=user_input.last_name,
        phone=user_input.phone,
        email=user_input.email,
        score=user_input.score,
    )
    user_id = InMemoryDatabase.create_user(user)

    UserHistory.create_user_history(user_id)

    return Response(
        dumps(
            {
                "id": user_id,
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


@app.get("/user/<int:user_id>/")
def get_user(user_id: int) -> Response:
    try:
        user = InMemoryDatabase.get_user(user_id)
    except KeyError:
        return Response("Нету пользователя с таким id", status=HTTPStatus.NOT_FOUND)
    return Response(
        dumps(
            {
                "id": user_id,
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

    user_history = UserHistory.get_user_history(user_id)

    return Response(
        dumps(user_history),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
