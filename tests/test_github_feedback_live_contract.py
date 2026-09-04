from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_latest_feedback_starts_available_after_post():
    post_response = client.post(
        "/v1/github/feedback",
        json={
            "name": "pytest",
            "conclusion": "failure",
            "summary": "1 test failed",
            "details": "AssertionError",
            "file_path": "tests/test_total.py",
            "line": 42,
        },
    )

    assert post_response.status_code == 200

    latest = client.get(
        "/v1/github/feedback/latest"
    )

    assert latest.status_code == 200

    payload = latest.json()

    assert payload["changed"] is True
    assert payload["feedback"]["concept"] == "TEST"
    assert payload["feedback"]["where_to_look"] == (
        "tests/test_total.py:42"
    )


def test_frontend_polls_latest_feedback():
    from pathlib import Path

    js = Path(
        "src/code2plain/web/static/app.js"
    ).read_text(
        encoding="utf-8"
    )

    assert "/v1/github/feedback/latest" in js
    assert "showGitHubFeedback" in js
