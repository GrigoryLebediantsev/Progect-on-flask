import
from app import app, USERS, models
from flask import request, Response
from http import HTTPStatus
from json import dumps


@app.route("/")
def index():
    return "<h1>Hello world</h2>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    # todo check phone and email validity

    user = models.User(id, first_name, last_name, phone, email)
    USERS.append(user)
    response = Response(
        dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

@app.get('/user/<int:user_id>/')
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
