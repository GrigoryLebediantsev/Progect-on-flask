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
            "Более двух операций поддерживаются только для умножения, возведения в степень и сложения",
            status=HTTPStatus.BAD_REQUEST,
        )

    min_num = data["min"]
    max_num = data["max"]
    values = [random.randint(min_num, max_num) for _ in range(count_nums)]

    try:
        expression = Expression(expr_id, operation, *values)
    except ValueError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)

    EXPRS.append(expression)

    return Response(
        dumps({"id": expression.id, "values": values}),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/math/<int:expr_id>")
def get_expr(expr_id):

    try:
        expression = EXPRS[expr_id]
    except IndexError:
        return Response(
            "Не найдено выражения с таким id", status=HTTPStatus.BAD_REQUEST
        )
    except ValueError:
        return Response("Некорректный тип данных для id", status=HTTPStatus.BAD_REQUEST)

    return Response(
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


@app.post("/math/<int:expr_id>/solve")
def solve_expr(expr_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    try:
        expression = EXPRS[expr_id]
    except IndexError:
        return Response(
            "Не существует выражения с таким id", status=HTTPStatus.BAD_REQUEST
        )

    try:
        user = USERS[user_id]
    except IndexError:
        return Response(
            "Не существует пользователя с таким id", status=HTTPStatus.BAD_REQUEST
        )

    result = expression.check_answer(user_answer)

    user.add_to_history(expression.to_dict(), user_answer)  # Очень не нравится этот момент

    if result == "correct":
        user.increase_score(expression.reward)
        reward = expression.reward
    else:
        reward = 0


    return Response(
        dumps({"expr_id": expr_id, "resault": result, "reward": reward}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
