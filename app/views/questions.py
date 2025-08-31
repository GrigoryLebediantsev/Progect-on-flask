from pydantic import ValidationError
from app import app
from flask import request, Response
from http import HTTPStatus
from json import dumps
from app.services.answer_checker import AnswerChecker
from app.adapter.in_memory import InMemoryDatabase
from app.dto.questions import GenerateQuestionInput
from app.services.question_servise import QuestionServise
from app.dto.question_solve import SolveQuestionInput


@app.post("/questions/create")
def create_question():
    data = request.get_json()

    try:
        question_input = GenerateQuestionInput(**data)
    except ValidationError as e:
        return Response(str(e), status=HTTPStatus.BAD_REQUEST)

    question = QuestionServise.create_question(question_input)
    question_output = question.to_dict(question_id=question.id)

    return Response(dumps(question_output), status=HTTPStatus.OK, content_type="application/json")



@app.get("/questions/random")
def random_quest(): # todo добавить проверку на  существование вопросов в целом
    question_id = InMemoryDatabase.get_random_quest_id()
    question = InMemoryDatabase.get_question(question_id)
    return Response(
        dumps(
            {
                "id": question_id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@app.post("/questions/<int:question_id>/solve")
def solve_quest(question_id):
    data = request.get_json()

    input_dto = SolveQuestionInput(**data, question_id=question_id)

    result, reward = AnswerChecker.check_question_answer(input_dto)

    return Response(
        dumps(
            {
                "question_id": question_id,
                "result": result,
                "reward": reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
