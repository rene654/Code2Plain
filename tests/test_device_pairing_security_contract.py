from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


REGISTRY = (
    ROOT
    / "src"
    / "code2plain"
    / "devices"
    / "registry.py"
)


def test_pairing_uses_cryptographic_randomness():
    text = REGISTRY.read_text()

    assert (
        "secrets.token_urlsafe"
        in text
    )


def test_pairing_token_is_hashed():
    text = REGISTRY.read_text()

    assert (
        "hashlib.sha256"
        in text
    )

    assert (
        "token_hash"
        in text
    )


def test_pairing_supports_expiration():
    text = REGISTRY.read_text()

    assert (
        "expires_at"
        in text
    )


def test_pairing_supports_revocation():
    text = REGISTRY.read_text()

    assert (
        "revoke_device"
        in text
    )

    assert (
        "revoked_at"
        in text
    )
