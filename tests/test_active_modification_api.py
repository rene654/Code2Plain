from fastapi.testclient import TestClient

from code2plain.api.app import app
from tests.demo_test_helper import demo_credentials

client = TestClient(app)
def test_correct_active_modification_answer():
    user_id, token = demo_credentials(client)
    response = client.post(
        "/v1/learning/modification-answer",
        json={
            "user_id": user_id,
            "demo_token": token,
            "code": (
                'high_value = sales['
                'sales["amount"] > 1000]'
            ),
            "answer": (
                'high_value = sales['
                'sales["amount"] > 1500]'
            ),
        },
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True
def test_incorrect_active_modification_answer():
    user_id, token = demo_credentials(client)
    response = client.post(
        "/v1/learning/modification-answer",
        json={
            "user_id": user_id,
            "demo_token": token,
            "code": (
                'high_value = sales['
                'sales["amount"] > 1000]'
            ),
            "answer": (
                'high_value = sales['
                'sales["amount"] > 1200]'
            ),
        },
    )
    assert response.status_code == 200
    assert response.json()["correct"] is False
