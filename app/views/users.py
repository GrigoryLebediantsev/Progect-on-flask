from app import app, USERS, models
from flask import request, Response
from http import HTTPStatus
from json import dumps


@app.post("/user/create")
def user_create():
    data = request.get_json() or {}
    user_id = len(USERS)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone")
    email = data.get("email")

    try:
        user = models.User(user_id, first_name, last_name, phone, email)
    except ValueError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)

    USERS.append(user)
    response = Response(
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
    return response


@app.get("/user/<int:user_id>/")
def get_user(user_id):

    if user_id < 0 or user_id >= len(USERS):
        return Response(
            "Не найдено пользователя с таким id", status=HTTPStatus.NOT_FOUND
        )
    try:
        user = USERS[user_id]
    except IndexError:
        return Response(
            "Не найдено пользователя с таким id", status=HTTPStatus.NOT_FOUND
        )
    except ValueError:
        return Response(
            "Не найдено пользователя с таким id", status=HTTPStatus.NOT_FOUND
        )

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
def get_history(user_id):

    try:
        user = USERS[user_id]
    except IndexError:
        return Response("Нету пользователя с таким id", status=HTTPStatus.BAD_REQUEST)

    print(user.history)
    return Response(dumps({"history": user.history}), status=HTTPStatus.OK, mimetype='application/json')




