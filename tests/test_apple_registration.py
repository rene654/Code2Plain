from datetime import (
    datetime,
    timezone,
)

import pytest

from code2plain.devices import (
    ApplePushRegistrationService,
    ApplePushRegistry,
    DeviceRegistry,
)


BASE = datetime(
    2026,
    8,
    16,
    12,
    0,
    tzinfo=timezone.utc,
)


def make_service(
    tmp_path,
):
    database = (
        tmp_path
        / "devices.db"
    )

    device_registry = (
        DeviceRegistry(
            database
        )
    )

    apple_registry = (
        ApplePushRegistry(
            database
        )
    )

    return (
        device_registry,
        apple_registry,
        ApplePushRegistrationService(
            device_registry,
            apple_registry,
        ),
    )


def test_pairing_token_registers_apple_endpoint(
    tmp_path,
):

    (
        device_registry,
        apple_registry,
        service,
    ) = make_service(
        tmp_path
    )

    pairing = (
        device_registry
        .create_pairing_request(
            "learner_1"
        )
    )

    result = service.register(
        pairing_token=(
            pairing.token
        ),
        apns_token="apns123",
        bundle_id=(
            "com.code2plain.app"
        ),
        environment="sandbox",
    )

    assert (
        result.status
        == "connected"
    )

    endpoint = (
        apple_registry.get(
            result.device_id
        )
    )

    assert endpoint is not None

    assert (
        endpoint.apns_token
        == "apns123"
    )


def test_pairing_token_cannot_be_reused(
    tmp_path,
):

    (
        device_registry,
        _,
        service,
    ) = make_service(
        tmp_path
    )

    pairing = (
        device_registry
        .create_pairing_request(
            "learner_1"
        )
    )

    service.register(
        pairing_token=(
            pairing.token
        ),
        apns_token="apns123",
        bundle_id=(
            "com.code2plain.app"
        ),
    )

    with pytest.raises(
        ValueError
    ):
        service.register(
            pairing_token=(
                pairing.token
            ),
            apns_token="apns456",
            bundle_id=(
                "com.code2plain.app"
            ),
        )
