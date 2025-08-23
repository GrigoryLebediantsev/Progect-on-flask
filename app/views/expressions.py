from app.models.expressions import Expression
from app import app, USERS, EXPRS
from flask import request, Response
from http import HTTPStatus
from json import dumps
import random


@app.get("/math/expression")
def generate_expr():
    data = request.get_json()
    expr_id = len(EXPRS)
    count_nums = data["count_nums"]
    operation = Expression.choose_operation(data["operation"])

    if not Expression.validate_expression_params(count_nums, operation):
        return Response(
            "Более двух операций поддерживаются только для умножения возведения в степень и сложения",
            status=HTTPStatus.BAD_REQUEST,
        )

    min_num = data["min"]
    max_num = data["max"]
    values = [random.randint(min_num, max_num) for _ in range(count_nums)]

    try:
        expression = Expression(expr_id, operation, *values)
    except ValueError:
        return Response(status=HTTPStatus.BAD_REQUEST)

    EXPRS.append(expression)
    return Response(
        dumps({"id": expression.id, "values": values}),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/math/<int:expr_id>")
def get_expr(expr_id):
    if expr_id > len(EXPRS) - 1 or expr_id < 0:
        return Response(
            "id вышел за границы существоующих выражений", status=HTTPStatus.NOT_FOUND
        )
    expression = EXPRS[expr_id]
    response = Response(
        dumps(
            {
                "id": expression.id,
                "values": expression.values,
                "operation": expression.operation,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/math/<int:expr_id>/solve")
def solve_expr(expr_id):

    if expr_id > len(EXPRS) - 1 or expr_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)

    data = request.get_json()
    user_id = data["user_id"]

    if user_id > len(USERS) - 1 or user_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)

    user_answer = data["user_answer"]
    expression = EXPRS[expr_id]
    user = USERS[user_id]
    result = expression.check_answer(user_answer, user)
    response = Response(
        dumps({"expr_id": expr_id, "resault": result, "reward": expression.reward}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
