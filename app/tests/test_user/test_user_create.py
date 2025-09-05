import pytest
from app import app
from http import HTTPStatus


def create_user_payload(
    first_name: str, last_name: str, phone: str, email: str
) -> dict:
    return {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
    }


def user_in_memory(client, user_id):
    url = f"/users/{user_id}/"
    request_user = client.get(url)
    return request_user.status_code == HTTPStatus.OK


def create_user_history(client, user_id):
    url = f"/users/{user_id}/history"
    request_history = client.get(url)
    return request_history.status_code == HTTPStatus.OK


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_user_create(client):
    payload = create_user_payload(
        "Vasya", "Pupkin", "+79999999999", "leb6370031zet@gmail.com"
    )

    url_post = "/users/create"
    create_response = client.post(url_post, json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_id = create_response.get_json()["id"]

    assert create_response.get_json()["first_name"] == payload["first_name"]
    assert create_response.get_json()["last_name"] == payload["last_name"]
    assert create_response.get_json()["phone"] == payload["phone"]
    assert create_response.get_json()["email"] == payload["email"]

    assert user_in_memory(client, user_id)

    assert create_user_history(client, user_id)


def test_create_user_bad_data(client):
    url_post = "/users/create"
    payload_wrong_phone = create_user_payload(
        "Vasya", "Pupkin", "1234567891", "leb6370031zet@gmail.com"
    )

    payload_wrong_email = create_user_payload(
        "Vasya", "Pupkin", "+79999999999", "leb6370031"
    )

    payload_wrong_first_name = create_user_payload(
        "vasya", "Pupkin", "+79999999999", "leb6370031zet@gmail.com"
    )

    payload_wrong_last_name = create_user_payload(
        "Vasya", "pupkin", "+79999999999", "leb6370031zet@gmail.com"
    )

    request_wrong_phone = client.post(url_post, json=payload_wrong_phone)
    request_wrong_email = client.post(url_post, json=payload_wrong_email)
    request_wrong_first_name = client.post(url_post, json=payload_wrong_first_name)
    request_wrong_last_name = client.post(url_post, json=payload_wrong_last_name)

    assert request_wrong_phone.status_code == HTTPStatus.BAD_REQUEST
    assert request_wrong_email.status_code == HTTPStatus.BAD_REQUEST
    assert request_wrong_first_name.status_code == HTTPStatus.BAD_REQUEST
    assert request_wrong_last_name.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_incomplete_request(client):
    url_post = "/users/create"
    payload_incomplete_first_name = {
        "last_name": "Pupkin",
        "phone": "+79999999999",
        "email": "mail@gmail.com",
    }

    payload_incomplete_last_name = {
        "first_name": "Vasya",
        "phone": "+79999999999",
        "email": "mail@gmail.com",
    }

    payload_incomplete_phone = {
        "first_name": "Vasya",
        "last_name": "Pupkin",
        "email": "mail@gmail.com",
    }

    payload_incomplete_email = {
        "first_name": "Vasya",
        "last_name": "Pupkin",
        "phone": "+79999999999",
    }

    request_incomplete_phone = client.post(url_post, json=payload_incomplete_phone)
    request_incomplete_email = client.post(url_post, json=payload_incomplete_email)
    request_incomplete_first_name = client.post(
        url_post, json=payload_incomplete_first_name
    )
    request_incomplete_last_name = client.post(
        url_post, json=payload_incomplete_last_name
    )

    assert request_incomplete_phone.status_code == HTTPStatus.BAD_REQUEST
    assert request_incomplete_email.status_code == HTTPStatus.BAD_REQUEST
    assert request_incomplete_first_name.status_code == HTTPStatus.BAD_REQUEST
    assert request_incomplete_last_name.status_code == HTTPStatus.BAD_REQUEST
