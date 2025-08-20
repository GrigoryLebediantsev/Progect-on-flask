from app import app, USERS, models, EXPRS
from flask import request, Response
from http import HTTPStatus
from json import dumps
import random


@app.route("/")
def index():
    return "<h1>Hello world</h2>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    if not models.User.validate_emile(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.User.validate_phone(phone):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(user_id, first_name, last_name, phone, email)
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
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/expression")
def generate_expr():
    data = request.get_json()
    expr_id = len(EXPRS)
    count_nums = data["count_nums"]
    operation = data["operation"]
    min_num = data["min"]
    max_num = data["max"]

    if operation == "random":
        operation = random.choice(["+", "*", "-", "//", "**"])

    if count_nums <= 1 or (count_nums > 2 and operation not in {"+", "*"}):
        return Response(status=HTTPStatus.BAD_REQUEST)

    values = [random.randint(min_num, max_num) for _ in range(count_nums)]

    expression = models.Expression(expr_id, operation, *values)
    EXPRS.append(expression)
    response = Response(
        dumps(
            {
                "id": expression.id,
                "values": values,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/<int:expr_id>")
def ger_expr(expr_id):
    if expr_id > len(EXPRS) - 1 or expr_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)
    expression = EXPRS[expr_id]
    response = Response(
        dumps(
            {
                "id": expression.id,
                "values": expression.values,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
