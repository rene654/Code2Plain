from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_learning_answer_endpoint_returns_feedback():
    response = client.post(
        "/v1/learning/answer",
        json={
            "user_id": "api-user",
            "skill_id": "METHOD_CALL",
            "correct": True,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["skill_id"] == "METHOD_CALL"
    assert payload["correct"] >= 1
    assert "message" in payload
    assert "next_step" in payload


def test_learning_answer_endpoint_is_user_specific():
    response = client.post(
        "/v1/learning/answer",
        json={
            "user_id": "isolated-user",
            "skill_id": "INPUT_OUTPUT",
            "correct": False,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["incorrect"] >= 1
