from fastapi.testclient import TestClient

from code2plain.api.app import app
from tests.demo_test_helper import demo_credentials


client = TestClient(app)


def test_public_check_does_not_reveal_answer_key():
    user_id, token = demo_credentials(
        client
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "user_id":
                user_id,
            "demo_token":
                token,
            "code": (
                'result = active'
                '.groupby("customer_id")'
                '["amount"].sum()'
            )
        },
    )

    assert response.status_code == 200

    check = response.json()[
        "items"
    ][0]["check"]

    assert "correct_index" not in check


def test_correct_selection_is_verified_server_side():
    _, token = demo_credentials(
        client,
        "quiz-user-correct",
    )

    response = client.post(
        "/v1/learning/check-answer",
        json={
            "user_id":
                "quiz-user-correct",
            "skill_id":
                "DATA_GROUPING",
            "code": (
                'result = active'
                '.groupby("customer_id")'
                '["amount"].sum()'
            ),
            "input_from":
                "active",
            "output_to":
                "result",
            "selected_index":
                0,
            "demo_token":
                token,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["correct"] is True
    assert payload["explanation"]


def test_wrong_selection_is_verified_server_side():
    _, token = demo_credentials(
        client,
        "quiz-user-wrong",
    )

    response = client.post(
        "/v1/learning/check-answer",
        json={
            "user_id":
                "quiz-user-wrong",
            "skill_id":
                "DATA_GROUPING",
            "code": (
                'result = active'
                '.groupby("customer_id")'
                '["amount"].sum()'
            ),
            "input_from":
                "active",
            "output_to":
                "result",
            "selected_index":
                2,
            "demo_token":
                token,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["correct"] is False

    assert (
        payload["mastery_level"]
        == "reforzar"
    )


def test_invalid_selection_is_rejected():
    _, token = demo_credentials(
        client,
        "quiz-user-invalid",
    )

    response = client.post(
        "/v1/learning/check-answer",
        json={
            "user_id":
                "quiz-user-invalid",
            "skill_id":
                "DATA_GROUPING",
            "code":
                'result = active.groupby("id").sum()',
            "input_from":
                "active",
            "output_to":
                "result",
            "selected_index":
                9,
            "demo_token":
                token,
        },
    )

    assert response.status_code == 400
