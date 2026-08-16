from datetime import (
    datetime,
    timezone,
)

from code2plain.devices import (
    ApplePushRegistry,
)
from code2plain.notifications import (
    APNsNotificationProvider,
    APNsRequest,
    APNsTransport,
    NotificationMessage,
)


BASE = datetime(
    2026,
    8,
    16,
    12,
    0,
    tzinfo=timezone.utc,
)


class FakeAPNsTransport(
    APNsTransport
):
    def __init__(self):
        self.requests = []


    def send(
        self,
        request: APNsRequest,
    ) -> str:

        self.requests.append(
            request
        )

        return "apns_test_message_1"


def test_apple_endpoint_can_be_registered(
    tmp_path,
):
    registry = ApplePushRegistry(
        tmp_path / "devices.db"
    )

    endpoint = registry.register(
        device_id="device_1",
        apns_token="abc123",
        bundle_id="com.code2plain.app",
        environment="sandbox",
        now=BASE,
    )

    assert endpoint.is_active
    assert endpoint.device_id == "device_1"
    assert endpoint.apns_token == "abc123"


def test_apns_provider_resolves_device_endpoint(
    tmp_path,
):
    registry = ApplePushRegistry(
        tmp_path / "devices.db"
    )

    registry.register(
        device_id="device_1",
        apns_token="abc123",
        bundle_id="com.code2plain.app",
        now=BASE,
    )

    transport = FakeAPNsTransport()

    provider = APNsNotificationProvider(
        registry,
        transport,
    )

    result = provider.send(
        NotificationMessage(
            device_id="device_1",
            title="Code2Plain",
            body="Learning digest ready.",
        )
    )

    assert result.success
    assert result.provider == "apns"

    assert len(
        transport.requests
    ) == 1

    request = transport.requests[0]

    assert request.apns_token == "abc123"

    assert (
        request.bundle_id
        == "com.code2plain.app"
    )


def test_revoked_endpoint_receives_no_push(
    tmp_path,
):
    registry = ApplePushRegistry(
        tmp_path / "devices.db"
    )

    registry.register(
        device_id="device_1",
        apns_token="abc123",
        bundle_id="com.code2plain.app",
        now=BASE,
    )

    registry.revoke(
        "device_1",
        now=BASE,
    )

    provider = APNsNotificationProvider(
        registry,
        FakeAPNsTransport(),
    )

    result = provider.send(
        NotificationMessage(
            device_id="device_1",
            title="Code2Plain",
            body="Digest ready.",
        )
    )

    assert not result.success


def test_missing_endpoint_is_blocked(
    tmp_path,
):
    provider = APNsNotificationProvider(
        ApplePushRegistry(
            tmp_path / "devices.db"
        ),
        FakeAPNsTransport(),
    )

    result = provider.send(
        NotificationMessage(
            device_id="missing",
            title="Code2Plain",
            body="Digest ready.",
        )
    )

    assert not result.success
