from __future__ import annotations

from dataclasses import dataclass

from code2plain.devices import (
    ApplePushRegistry,
)
from code2plain.notifications.models import (
    NotificationMessage,
    NotificationResult,
)
from code2plain.notifications.provider import (
    NotificationProvider,
)


@dataclass(frozen=True)
class APNsRequest:
    device_id: str
    apns_token: str
    bundle_id: str
    environment: str
    title: str
    body: str


class APNsTransport:
    """
    Transport boundary for Apple Push Notification service.

    Real HTTP/2 + token authentication is added after
    Apple credentials are configured.
    """

    def send(
        self,
        request: APNsRequest,
    ) -> str:

        raise NotImplementedError(
            "Real APNs transport is not configured."
        )


class APNsNotificationProvider(
    NotificationProvider
):
    """
    NotificationProvider implementation for Apple devices.

    Resolves an internal Code2Plain device_id into the
    corresponding APNs endpoint.
    """

    def __init__(
        self,
        registry: ApplePushRegistry,
        transport: APNsTransport,
    ) -> None:

        self.registry = registry
        self.transport = transport


    def send(
        self,
        message: NotificationMessage,
    ) -> NotificationResult:

        endpoint = self.registry.get(
            message.device_id
        )

        if (
            endpoint is None
            or not endpoint.is_active
        ):
            return NotificationResult(
                success=False,
                provider="apns",
                device_id=message.device_id,
                error=(
                    "No active Apple push endpoint."
                ),
            )

        request = APNsRequest(
            device_id=message.device_id,
            apns_token=endpoint.apns_token,
            bundle_id=endpoint.bundle_id,
            environment=endpoint.environment,
            title=message.title,
            body=message.body,
        )

        try:
            message_id = self.transport.send(
                request
            )

        except Exception as error:
            return NotificationResult(
                success=False,
                provider="apns",
                device_id=message.device_id,
                error=str(
                    error
                ),
            )

        return NotificationResult(
            success=True,
            provider="apns",
            device_id=message.device_id,
            message_id=message_id,
        )
