from datetime import (
    datetime,
    timezone,
)

import jwt

from cryptography.hazmat.primitives.asymmetric.ec import (
    SECP256R1,
    generate_private_key,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from code2plain.notifications import (
    APNsAuthConfig,
    APNsJWTProvider,
)


BASE = datetime(
    2026,
    8,
    16,
    12,
    0,
    tzinfo=timezone.utc,
)


def create_private_key(
    tmp_path,
):
    private_key = (
        generate_private_key(
            SECP256R1()
        )
    )

    pem = private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.PKCS8,
        NoEncryption(),
    )

    path = (
        tmp_path
        / "AuthKey_TEST.p8"
    )

    path.write_bytes(
        pem
    )

    return path


def test_apns_auth_config_requires_existing_key(
    tmp_path,
):
    missing = (
        tmp_path
        / "missing.p8"
    )

    try:
        APNsAuthConfig(
            key_id="KEY123",
            team_id="TEAM123",
            private_key_path=missing,
        )

    except ValueError as error:
        assert (
            "does not exist"
            in str(error)
        )

    else:
        raise AssertionError(
            "Missing key must be rejected"
        )


def test_jwt_contains_apple_claims(
    tmp_path,
):
    path = create_private_key(
        tmp_path
    )

    provider = APNsJWTProvider(
        APNsAuthConfig(
            key_id="KEY123",
            team_id="TEAM123",
            private_key_path=path,
        )
    )

    token = provider.create_token(
        now=BASE
    )

    header = jwt.get_unverified_header(
        token
    )

    claims = jwt.decode(
        token,
        options={
            "verify_signature":
                False
        },
    )

    assert header["kid"] == "KEY123"

    assert (
        claims["iss"]
        == "TEAM123"
    )

    assert (
        claims["iat"]
        == int(
            BASE.timestamp()
        )
    )
