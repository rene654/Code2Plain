from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_learning_page_loads():
    response = client.get("/learn")

    assert response.status_code == 200
    assert "Code2Plain" in response.text
    assert "Explicar código" in response.text
    assert "/v1/context-block-learn" in response.text


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


def test_learning_page_accepts_github_url():
    response = client.get("/learn")

    assert response.status_code == 200
    assert "githubUrl" in response.text
    assert (
        "/v1/github-file/learn"
        in response.text
    )


def test_learning_page_keeps_manual_code_mode():
    response = client.get("/learn")

    assert (
        "/v1/context-block-learn"
        in response.text
    )


def test_learning_page_uses_context_blocks():
    response = client.get("/learn")

    assert response.status_code == 200
    assert (
        "/v1/context-block-learn"
        in response.text
    )


def test_learning_page_displays_zero_retention_notice():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "Tu código se procesa temporalmente "
        "y no se guarda"
        in response.text
    )

    assert (
        "Solo conservamos conceptos "
        "de aprendizaje y progreso"
        in response.text
    )

    assert (
        "¿Qué significa esto?"
        in response.text
    )
