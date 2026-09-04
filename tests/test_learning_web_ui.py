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


def test_learning_feedback_buttons_are_visible():
    response = client.get("/learn")

    assert response.status_code == 200


    assert "color: #171717" in response.text
    assert "background: #ffffff" in response.text


def test_learning_page_uses_spanish_why_label():
    response = client.get("/learn")

    assert "¿Por qué?" in response.text



def test_learning_page_has_compact_evaluable_check():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "Comprueba lo que entendiste"
        in response.text
    )

    assert (
        "/v1/learning/check-answer"
        in response.text
    )

    assert "Verificar" in response.text
    assert "learning-check" in response.text


def test_learning_page_uses_persistent_anonymous_identity():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "code2plain.learning_user_id"
        in response.text
    )

    assert (
        "getOrCreateLearningUserId"
        in response.text
    )

    assert (
        "localStorage"
        in response.text
    )

    assert (
        "learningUserId"
        in response.text
    )


def test_learning_page_does_not_share_default_user():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "default-user"
        not in response.text
    )


def test_learning_page_sends_user_identity_for_adaptation():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "user_id:"
        in response.text
    )

    assert (
        "learningUserId"
        in response.text
    )


def test_learning_page_exposes_visible_adaptive_policy():
    response = client.get("/learn")

    assert response.status_code == 200

    assert (
        "item.teaching_policy"
        in response.text
    )

    assert (
        "adaptive-note"
        in response.text
    )

    assert (
        'policy.level'
        in response.text
    )


def test_learning_page_exposes_twenty_minute_demo():
    response = client.get("/learn")

    assert response.status_code == 200

    assert "demoTimer" in response.text

    assert (
        "/v1/demo/start"
        in response.text
    )

    assert (
        "/v1/demo/status"
        in response.text
    )

    assert "demoToken" in response.text

    assert (
        "Demo 20:00"
        in response.text
    )


def test_expired_demo_is_not_automatically_reissued():
    response = client.get("/learn")

    assert response.status_code == 200

    text = response.text

    assert (
        "An expired token is NOT "
        "replaced automatically"
        in text
    )


def test_learning_page_exposes_owner_mode():
    response = client.get("/learn")

    assert response.status_code == 200

    assert "ownerAccessButton" in response.text
    assert "/v1/owner/login" in response.text
    assert "/v1/owner/status" in response.text
    assert "ownerToken" in response.text
    assert "Acceso completo" in response.text


def test_learning_page_sends_owner_token():
    response = client.get("/learn")

    assert response.status_code == 200

    assert "owner_token" in response.text
