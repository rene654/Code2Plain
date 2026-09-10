from fastapi.testclient import TestClient

from code2plain.api.app import app
from tests.demo_test_helper import demo_credentials

client = TestClient(app)


def test_beginner_exercise_correct_answer():
    user_id, token = demo_credentials(client)

    response = client.post(
        "/v1/learning/exercise-answer",
        json={
            "user_id": user_id,
            "demo_token": token,
            "code": 'sales = pd.read_csv("sales.csv")',
            "selected_index": 0,
        },
    )

    assert response.status_code == 200
    assert response.json()["correct"] is True
    assert response.json()["explanation"]


def test_beginner_exercise_wrong_answer():
    user_id, token = demo_credentials(client)

    response = client.post(
        "/v1/learning/exercise-answer",
        json={
            "user_id": user_id,
            "demo_token": token,
            "code": 'sales = pd.read_csv("sales.csv")',
            "selected_index": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["correct"] is False
