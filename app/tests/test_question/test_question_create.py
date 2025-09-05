import pytest
from app import app
from http import HTTPStatus
from typing import Optional, Any


def create_question_payload(
    title: str, description: str, type: str, answer: str | int, choices: Optional[list[str]] = None
) -> dict:
    result: dict[str, Any] = {
        "title": title,
        "description": description,
        "type": type,
        "answer": answer,
    }
    if not choices is None:
        result["choices"] = choices
    return result


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
