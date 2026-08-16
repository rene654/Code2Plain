from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "code2plain"
    assert data["version"] == "0.1.0"


def test_explain_endpoint():
    response = client.post(
        "/v1/explain",
        json={
            "code": (
                'import pandas as pd\n'
                'df = pd.read_excel("orders.xlsx")\n'
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "sections" in data
    assert len(data["sections"]) == 2


def test_explain_returns_visual_learning_contract():
    response = client.post(
        "/v1/explain",
        json={"code": "total = 100"},
    )

    assert response.status_code == 200

    section = response.json()["sections"][0]

    assert section["section_number"] == 1
    assert section["color_tag"] == "blue"
    assert section["what_it_does"]
    assert section["what_to_learn"]


def test_empty_code_is_rejected():
    response = client.post(
        "/v1/explain",
        json={"code": ""},
    )

    assert response.status_code == 422


def test_visual_learning_ui_is_available():
    response = client.get("/")

    assert response.status_code == 200

    assert "Code2Plain" in response.text
    assert "Turn code into something you can learn." in response.text


def test_stylesheet_is_available():
    response = client.get(
        "/static/styles.css"
    )

    assert response.status_code == 200

    assert ".code-section" in response.text
