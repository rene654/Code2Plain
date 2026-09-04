from code2plain.demo_access import (
    DemoAccessService,
)


def test_demo_token_is_valid_when_created():
    service = DemoAccessService(
        secret="test-secret-0123456789abcdef-0123456789",
        duration_minutes=20,
    )

    access = service.issue(
        user_id="anon-browser-123"
    )

    status = service.verify(
        access.token
    )

    assert status.valid is True

    assert (
        status.user_id
        == "anon-browser-123"
    )

    assert (
        0
        < status.remaining_seconds
        <= 1200
    )


def test_demo_duration_is_twenty_minutes():
    service = DemoAccessService(
        secret="test-secret-0123456789abcdef-0123456789",
        duration_minutes=20,
    )

    access = service.issue(
        user_id="demo-user"
    )

    assert (
        access.duration_minutes
        == 20
    )


def test_modified_token_is_rejected():
    service = DemoAccessService(
        secret="test-secret-0123456789abcdef-0123456789"
    )

    access = service.issue(
        user_id="demo-user"
    )

    modified = (
        access.token[:-2]
        + "xx"
    )

    status = service.verify(
        modified
    )

    assert status.valid is False


def test_other_secret_cannot_verify_token():
    issuer = DemoAccessService(
        secret="secret-a-0123456789abcdef-0123456789abcd"
    )

    verifier = DemoAccessService(
        secret="secret-b-0123456789abcdef-0123456789abcd"
    )

    access = issuer.issue(
        user_id="demo-user"
    )

    status = verifier.verify(
        access.token
    )

    assert status.valid is False
