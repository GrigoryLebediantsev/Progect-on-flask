from pydantic import ValidationError
from app.services.answer_checker import AnswerChecker
from app.adapter.in_memory import InMemoryDatabase
from app.dto.expressions import GenerateExpressionInput
from app import app
from flask import request, Response
from http import HTTPStatus
from json import dumps
from app.services.expression_servise import ExpressionServise


@app.get("/math/expression")
def generate_expr() -> Response:    # ok
    try:
        expression_input = GenerateExpressionInput(**request.get_json())
    except ValidationError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)

    expression, expression_id = ExpressionServise.create_expression(expression_input)

    return Response(
        dumps({"id": expression_id, "values": expression.values}),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/math/<int:expression_id>")  # ok
def get_expr(expression_id: int) -> Response:

    try:
        expression = InMemoryDatabase.get_expression(expression_id)
    except KeyError:
        return Response(
            "Не существует выражения с таким id", status=HTTPStatus.NOT_FOUND
        )

    return Response(
        dumps(
            {
                "id": expression_id,
                "values": expression.values,
                "operation": expression.operation,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/math/<int:expression_id>/solve")
def solve_expr(expression_id: int) -> Response:

    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    result, reward = AnswerChecker.check_expression_answer(expression_id, user_id, user_answer)

    return Response(
        dumps({"expr_id": expression_id, "result": result, "reward": reward}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
