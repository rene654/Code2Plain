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

    normalized = " ".join(
        response.text.split()
    )

    assert (
        "Tu código se procesa temporalmente "
        "y no se guarda"
        in normalized
    )

    assert (
        "Solo conservamos conceptos "
        "de aprendizaje y progreso"
        in normalized
    )

    assert (
        "¿Qué significa esto?"
        in response.text
    )


def test_learning_page_exposes_human_feedback_endpoint():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "/v1/learning/answer"
        in response.text
    )

    assert (
        "sendLearningFeedback"
        in response.text
    )


def test_learning_page_shows_skill_self_assessment():
    response = client.get("/learn")

    assert response.status_code == 200

    assert "Estás practicando:" in response.text
    assert "La respondí bien" in response.text
    assert "Necesito repasarlo" in response.text


def test_learning_feedback_buttons_are_visible():
    response = client.get("/learn")

    assert response.status_code == 200

    assert "La respondí bien" in response.text
    assert "Necesito repasarlo" in response.text

    assert "color: #171717" in response.text
    assert "background: #ffffff" in response.text


def test_learning_page_uses_spanish_why_label():
    response = client.get("/learn")

    assert "¿Por qué?" in response.text
