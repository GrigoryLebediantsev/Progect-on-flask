from app import app, models, QUESTIONS
from flask import request, Response
from http import HTTPStatus
from json import dumps
import random


@app.post("/questions/create")
def create_question():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = len(QUESTIONS)

    if question_type == "ONE-ANSWER":
        answer = data["answer"]
        if not models.OneAnswer.is_valid(answer):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.OneAnswer(question_id, title, description, answer)
        QUESTIONS.append(question)
        response = Response(
            dumps(
                {
                    "id": question.id,
                    "title": question.title,
                    "description": question.description,
                    "type": question_type,
                    "answer": question.answer,
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]
        answer = data["answer"]
        if not models.MultipyChoice.is_valid(answer, choices):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.MultipyChoice(
            question_id, title, description, choices, answer
        )
        QUESTIONS.append(question)
        response = Response(
            dumps(
                {
                    "id": question.id,
                    "title": question.title,
                    "description": question.description,
                    "type": question_type,
                    "choices": question.choices,
                    "answer": question.answer,
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    return response


@app.get("/questions/random")
def random_quest():
    if len(QUESTIONS) == 0:
        return Response("There not questions", status=HTTPStatus.NOT_FOUND)
    quest_id = random.randint(0, len(QUESTIONS) - 1)
    question = QUESTIONS[quest_id]
    return Response(
        dumps(
            {
                "id": question.id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
