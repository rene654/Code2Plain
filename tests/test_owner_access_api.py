from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_owner_login_rejects_invalid_credential(
    monkeypatch,
):
    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SECRET",
        "owner-secret",
    )

    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SIGNING_SECRET",
        "owner-signing-secret-0123456789abcdef",
    )

    from code2plain import owner_access

    owner_access.owner_access_service.secret = (
        "owner-secret"
    )

    owner_access.owner_access_service.signing_secret = (
        "owner-signing-secret-0123456789abcdef"
    )

    response = client.post(
        "/v1/owner/login",
        json={
            "credential":
                "wrong-secret",
        },
    )

    assert response.status_code == 403


def test_owner_login_returns_session(
    monkeypatch,
):
    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SECRET",
        "owner-secret",
    )

    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SIGNING_SECRET",
        "owner-signing-secret-0123456789abcdef",
    )

    from code2plain import owner_access

    owner_access.owner_access_service.secret = (
        "owner-secret"
    )

    owner_access.owner_access_service.signing_secret = (
        "owner-signing-secret-0123456789abcdef"
    )

    response = client.post(
        "/v1/owner/login",
        json={
            "credential":
                "owner-secret",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["token"]
    assert payload["expires_at"]


def test_owner_session_allows_learning(
    monkeypatch,
):
    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SECRET",
        "owner-secret",
    )

    monkeypatch.setenv(
        "CODE2PLAIN_OWNER_SIGNING_SECRET",
        "owner-signing-secret-0123456789abcdef",
    )

    from code2plain import owner_access

    owner_access.owner_access_service.secret = (
        "owner-secret"
    )

    owner_access.owner_access_service.signing_secret = (
        "owner-signing-secret-0123456789abcdef"
    )

    token = client.post(
        "/v1/owner/login",
        json={
            "credential":
                "owner-secret",
        },
    ).json()["token"]

    response = client.post(
        "/v1/context-block-learn",
        json={
            "user_id":
                "owner-user",
            "owner_token":
                token,
            "code":
                'print("hello")',
        },
    )

    assert response.status_code == 200
