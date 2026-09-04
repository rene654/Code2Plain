from code2plain.owner_access import (
    OwnerAccessService,
)


OWNER_SECRET = (
    "owner-secret-0123456789abcdef-0123456789abcd"
)

SIGNING_SECRET = (
    "signing-secret-0123456789abcdef-0123456789"
)


def _service() -> OwnerAccessService:
    return OwnerAccessService(
        secret=OWNER_SECRET,
        signing_secret=SIGNING_SECRET,
        session_hours=12,
    )


def test_correct_owner_credential_is_valid():
    service = _service()

    assert (
        service.verify_credential(
            OWNER_SECRET
        )
        is True
    )


def test_wrong_owner_credential_is_invalid():
    service = _service()

    assert (
        service.verify_credential(
            "wrong-secret"
        )
        is False
    )


def test_valid_owner_session_is_issued():
    service = _service()

    session = service.issue_session(
        OWNER_SECRET
    )

    assert session is not None
    assert session.token
    assert session.expires_at


def test_owner_session_verifies():
    service = _service()

    session = service.issue_session(
        OWNER_SECRET
    )

    assert session is not None

    status = service.verify_session(
        session.token
    )

    assert status.valid is True
    assert status.expires_at


def test_wrong_signing_secret_rejects_session():
    issuer = _service()

    verifier = OwnerAccessService(
        secret=OWNER_SECRET,
        signing_secret=(
            "different-signing-secret-"
            "0123456789abcdef-0123456789"
        ),
    )

    session = issuer.issue_session(
        OWNER_SECRET
    )

    assert session is not None

    status = verifier.verify_session(
        session.token
    )

    assert status.valid is False


def test_owner_access_disabled_without_secrets():
    service = OwnerAccessService(
        secret="",
        signing_secret="",
    )

    assert service.configured is False

    assert (
        service.verify_credential(
            "anything"
        )
        is False
    )
