from app import app, models, QUESTIONS, USERS
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
        return Response(
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
        return Response(
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
        return Response("Недопустимый тип вопроса", status=HTTPStatus.BAD_REQUEST)


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


@app.post("/questions/<int:question_id>/solve")
def solve_quest(question_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    try:
        question = QUESTIONS[question_id]
        user = USERS[user_id]
    except IndexError:
        return Response(
            "Неправильный индекс у пользователя или вопроса",
            status=HTTPStatus.BAD_REQUEST,
        )

    user.add_to_history(question.to_dict(), user_answer)

    if question.answer == user_answer:
        user.increase_score(question.reward)
        result = "Correct"
        reward = question.reward
    else:
        result = "Wrong"
        reward = 0

    return Response(
        dumps(
            {
                "question_id": question.id,
                "result": result,
                "reward": reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype='application/json'
    )
