from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_github_feedback_api_returns_compact_failure():
    response = client.post(
        "/v1/github/feedback",
        json={
            "name": "pytest",
            "conclusion": "failure",
            "summary": "2 tests failed",
            "details": (
                "AssertionError: expected 10 "
                "but received 8"
            ),
            "file_path": "tests/test_total.py",
            "line": 42,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "failed"
    assert payload["headline"] == "Algo salió mal"
    assert payload["concept"] == "TEST"
    assert payload["where_to_look"] == (
        "tests/test_total.py:42"
    )


def test_github_feedback_api_handles_import_failure():
    response = client.post(
        "/v1/github/feedback",
        json={
            "name": "python tests",
            "conclusion": "failure",
            "summary": (
                "ModuleNotFoundError: "
                "No module named 'pandas'"
            ),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["concept"] == "IMPORT"
