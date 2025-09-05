import pytest
from app import app
from .test_user_create import create_user_payload
from http import HTTPStatus


def get_user_str_id(client, user_id: int):
    url_get = f"/users/{str(user_id)}/"
    get_response = client.get(url_get)
    return get_response.status_code == HTTPStatus.OK


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_user_get(client):
    payload = create_user_payload(
        "Vasya", "Pupkin", "+79999999999", "leb6370031zet@gmail.com"
    )
    url_post = "/users/create"
    create_response = client.post(url_post, json=payload)

    user_id = create_response.get_json()["id"]

    url_get = f"/users/{user_id}/"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.OK
    assert get_user_str_id(client, user_id)
    user_data = get_response.get_json()

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["phone"] == payload["phone"]
    assert user_data["email"] == payload["email"]


def test_bad_user_get(client):
    user_id_1 = 1
    url_get = f"/users/{user_id_1}/"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.NOT_FOUND

    user_id_2 = "1"
    url_get = f"/users/{user_id_2}/"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.NOT_FOUND

    user_id_3 = "a"
    url_get = f"/users/{user_id_3}/"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_incomplete_user_get(client):
    user_id = ""
    url_get = f"/users/{user_id}/"
    get_response = client.get(url_get)
    assert get_response.status_code == HTTPStatus.NOT_FOUND
