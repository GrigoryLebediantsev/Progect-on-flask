from app.services import AnswerChecker, ExpressionCreateService
from app.adapter import InMemoryDatabase
from app import dto
from app.exceptions import ExpressionNotFoundError

from app.application import app

from flask import request, Response
from http import HTTPStatus
from json import dumps
from pydantic import ValidationError


@app.get("/math/expression")
def generate_expr() -> Response:  # ok
    data = request.get_json()
    try:
        expression_input = dto.GenerateExpressionInput(
            count_nums=data["count_nums"],
            operation=data["operation"],
            min=data["min"],
            max=data["max"],
        )
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    expression = ExpressionCreateService.create_expression(
        operation=expression_input.operation,
        values=expression_input.values,
        reward=expression_input.reward,
    )

    return Response(
        dumps({"id": expression.id, "values": expression.values}),
        HTTPStatus.OK,
        mimetype="application/json",
    )


@app.get("/math/<int:expression_id>")  # ok
def get_expr(expression_id: int) -> Response:

    try:
        expression = InMemoryDatabase.get_expression(expression_id)
    except ExpressionNotFoundError:
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
        input_dto = dto.SolveExpressionInput(
            user_id=data["user_id"],
            user_answer=data["user_answer"],
            expression_id=expression_id,
        )
    except ValidationError:
        return Response("Ошибка запроса", status=HTTPStatus.BAD_REQUEST)

    result, reward = AnswerChecker.check_expression_answer(**input_dto.model_dump())

    return Response(
        dumps({"expr_id": expression_id, "result": result, "reward": reward}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
