from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "code2plain"
    assert data["version"] == "1.0.0"


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
    assert "Convierte código en algo que realmente puedas entender." in response.text


def test_stylesheet_is_available():
    response = client.get(
        "/static/styles.css"
    )

    assert response.status_code == 200

    assert ".code-section" in response.text


def test_explain_endpoint_accepts_language():
    response = client.post(
        "/v1/explain",
        json={
            "code": (
                'late_orders = '
                'df[df["status"] == "Late"]'
            ),
            "language": "fr",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["language"]
        == "fr"
    )

    assert (
        data["sections"][0]
        ["concept_label"]
        == "FILTRER (FILTER)"
    )


def test_live_endpoint_is_session_aware():
    import importlib
    import uuid

    api_module = importlib.import_module(
        "code2plain.api.app"
    )

    session_a = (
        "test-a-"
        + uuid.uuid4().hex[:8]
    )

    session_b = (
        "test-b-"
        + uuid.uuid4().hex[:8]
    )

    api_module._live_store.publish(
        {
            "code": "value_a = 1",
            "summary": "Session A",
            "sections": [],
            "language": "es",
        },
        source="test",
        session_id=session_a,
    )

    api_module._live_store.publish(
        {
            "code": "value_b = 2",
            "summary": "Session B",
            "sections": [],
            "language": "es",
        },
        source="test",
        session_id=session_b,
    )

    response_a = client.get(
        "/v1/live",
        params={
            "after": 0,
            "session_id": session_a,
        },
    )

    response_b = client.get(
        "/v1/live",
        params={
            "after": 0,
            "session_id": session_b,
        },
    )

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    payload_a = response_a.json()
    payload_b = response_b.json()

    assert (
        payload_a["session_id"]
        == session_a
    )

    assert (
        payload_b["session_id"]
        == session_b
    )

    assert (
        payload_a["explanation"]["summary"]
        == "Session A"
    )

    assert (
        payload_b["explanation"]["summary"]
        == "Session B"
    )


def test_live_endpoint_rejects_invalid_session():
    response = client.get(
        "/v1/live",
        params={
            "session_id":
                "invalid session!",
        },
    )

    assert response.status_code == 422
