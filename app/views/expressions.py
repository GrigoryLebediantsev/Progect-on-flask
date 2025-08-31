from pydantic import ValidationError
from app.services.answer_checker import AnswerChecker
from app.adapter.in_memory import InMemoryDatabase
from app.dto.expressions import GenerateExpressionInput
from app import app
from app.dto.expression_solve import SolveExpressionInput
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

    expression = ExpressionServise.create_expression(expression_input)

    return Response(
        dumps({"id": expression.id, "values": expression.values}),
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

    try:
        input_dto = SolveExpressionInput(**data, expression_id=expression_id)
    except ValidationError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)

    result, reward = AnswerChecker.check_expression_answer(input_dto)

    return Response(
        dumps({"expr_id": expression_id, "result": result, "reward": reward}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
