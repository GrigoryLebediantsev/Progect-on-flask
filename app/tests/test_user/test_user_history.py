from http import HTTPStatus
import pytest
from app import app
from .test_user_create import create_user_payload
from app.tests.test_expression.test_expression_create import create_expression_payload


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_user_history(client):
    user_payload = create_user_payload(
        "Vasya", "Pupkin", "+79999999999", "leb6370031zet@gmail.com"
    )
    user_url_post = "/users/create"
    user_create_response = client.post(user_url_post, json=user_payload)
    user_id = user_create_response.get_json()["id"]

    expression_payload = create_expression_payload(2, "+", 1, 10)
    expression_url_get = "/math/expression"
    expression_create_response =  client.get(expression_url_get, json=expression_payload)
    values = expression_create_response.get_json()["values"]
    expression_result = eval(" + ".join(map(str, values)))