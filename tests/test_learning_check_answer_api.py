from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_public_check_does_not_reveal_answer_key():
    response = client.post(
        "/v1/context-block-learn",
        json={
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
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["correct"] is True
    assert payload["explanation"]


def test_wrong_selection_is_verified_server_side():
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
        },
    )

    assert response.status_code == 400
