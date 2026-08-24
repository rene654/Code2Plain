from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_learning_page_loads():
    response = client.get("/learn")

    assert response.status_code == 200
    assert "Code2Plain" in response.text
    assert "Explicar código" in response.text
    assert "/v1/line-by-line" in response.text


def test_learning_page_has_inline_code_highlighting():
    response = client.get("/learn")

    assert response.status_code == 200
    assert (
        "code2plain-code-highlight"
        in response.text
    )
    assert (
        "appendColoredCode"
        in response.text
    )
