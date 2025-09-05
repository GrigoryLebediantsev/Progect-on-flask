import pytest
from app import app
from http import HTTPStatus


def create_expression_payload(
    count_nums: int, operation: str, min: int, max: int
) -> dict:
    return {
        "count_nums": count_nums,
        "operation": operation,
        "min": min,
        "max": max,
    }


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_expression_create(client):
    payload = create_expression_payload(2, "+", 1, 10)
    url_create = "/math/expression"
    create_response = client.get(url_create, json=payload)
    assert create_response.status_code == HTTPStatus.OK
    # values = create_response.get_json()["values"]
    # answer = eval(" + ".join(map(str, values)))
    expression_id = create_response.get_json()["id"]

    url_get = f"/math/{expression_id}"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.OK
    assert

