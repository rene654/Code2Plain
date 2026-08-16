from datetime import (
    datetime,
    timedelta,
    timezone,
)

import pytest

from code2plain.devices import (
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


def test_pairing_request_creates_one_time_token(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    request = registry.create_pairing_request(
        "learner_1",
        now=BASE,
    )

    assert request.token
    assert request.pairing_id.startswith(
        "pair_"
    )

    assert request.expires_at > BASE


def test_pairing_token_creates_device(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    request = registry.create_pairing_request(
        "learner_1",
        now=BASE,
    )

    device = registry.redeem_pairing_token(
        request.token,
        now=(
            BASE
            + timedelta(
                minutes=1
            )
        ),
    )

    assert device.device_id.startswith(
        "device_"
    )

    assert (
        device.learner_id
        == "learner_1"
    )

    assert device.is_active


def test_pairing_token_cannot_be_reused(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    request = registry.create_pairing_request(
        "learner_1",
        now=BASE,
    )

    registry.redeem_pairing_token(
        request.token,
        now=(
            BASE
            + timedelta(
                minutes=1
            )
        ),
    )

    with pytest.raises(
        ValueError,
        match="already used",
    ):
        registry.redeem_pairing_token(
            request.token,
            now=(
                BASE
                + timedelta(
                    minutes=2
                )
            ),
        )


def test_expired_pairing_token_is_rejected(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db",
        pairing_ttl_minutes=10,
    )

    request = registry.create_pairing_request(
        "learner_1",
        now=BASE,
    )

    with pytest.raises(
        ValueError,
        match="expired",
    ):
        registry.redeem_pairing_token(
            request.token,
            now=(
                BASE
                + timedelta(
                    minutes=11
                )
            ),
        )


def test_invalid_pairing_token_is_rejected(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    with pytest.raises(
        ValueError,
        match="invalid",
    ):
        registry.redeem_pairing_token(
            "not-a-real-token",
            now=BASE,
        )


def test_device_can_be_revoked(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    request = registry.create_pairing_request(
        "learner_1",
        now=BASE,
    )

    device = registry.redeem_pairing_token(
        request.token,
        now=(
            BASE
            + timedelta(
                minutes=1
            )
        ),
    )

    revoked = registry.revoke_device(
        device.device_id,
        now=(
            BASE
            + timedelta(
                minutes=2
            )
        ),
    )

    assert not revoked.is_active
    assert revoked.revoked_at is not None


def test_multiple_devices_can_belong_to_learner(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    for minute in (
        0,
        2,
    ):
        request = registry.create_pairing_request(
            "learner_1",
            now=(
                BASE
                + timedelta(
                    minutes=minute
                )
            ),
        )

        registry.redeem_pairing_token(
            request.token,
            now=(
                BASE
                + timedelta(
                    minutes=minute + 1
                )
            ),
        )

    devices = registry.list_devices(
        "learner_1"
    )

    assert len(devices) == 2
