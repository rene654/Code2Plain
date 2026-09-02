from uuid import uuid4

from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def _user() -> str:
    return (
        "demo-api-"
        + uuid4().hex
    )


def _token(
    user_id: str,
) -> str:
    response = client.post(
        "/v1/demo/start",
        json={
            "user_id":
                user_id,
        },
    )

    assert response.status_code == 200

    return response.json()[
        "token"
    ]


def test_demo_start_returns_twenty_minutes():
    user_id = _user()

    response = client.post(
        "/v1/demo/start",
        json={
            "user_id":
                user_id,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["token"]
    assert payload["expires_at"]

    assert (
        payload["duration_minutes"]
        == 20
    )


def test_demo_status_recognizes_valid_token():
    user_id = _user()

    token = _token(
        user_id
    )

    response = client.post(
        "/v1/demo/status",
        json={
            "token":
                token,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["valid"] is True

    assert (
        payload["user_id"]
        == user_id
    )

    assert (
        0
        < payload["remaining_seconds"]
        <= 1200
    )


def test_valid_demo_allows_learning():
    user_id = _user()

    token = _token(
        user_id
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "user_id":
                user_id,
            "demo_token":
                token,
            "code":
                'print("hello")',
        },
    )

    assert response.status_code == 200


def test_learning_without_demo_is_blocked():
    response = client.post(
        "/v1/context-block-learn",
        json={
            "user_id":
                _user(),
            "code":
                'print("hello")',
        },
    )

    assert response.status_code == 403


def test_demo_is_bound_to_its_user():
    owner = _user()

    token = _token(
        owner
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "user_id":
                _user(),
            "demo_token":
                token,
            "code":
                'print("hello")',
        },
    )

    assert response.status_code == 403
