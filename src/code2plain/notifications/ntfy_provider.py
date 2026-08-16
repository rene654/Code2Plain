from __future__ import annotations

import httpx

from code2plain.devices import (
    NtfyEndpointRegistry,
)
from code2plain.notifications.models import (
    NotificationMessage,
    NotificationResult,
)
from code2plain.notifications.provider import (
    NotificationProvider,
)


class NtfyNotificationProvider(
    NotificationProvider
):
    """
    Zero-cost physical delivery adapter.

    Messages are published using ntfy's JSON API so titles
    and learning content can safely contain Unicode.

    This adapter is for free physical validation and does
    not replace Code2Plain's native APNs implementation.
    """

    def __init__(
        self,
        registry: NtfyEndpointRegistry,
        *,
        timeout_seconds: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:

        self.registry = registry

        self._owns_client = (
            client is None
        )

        self.client = (
            client
            or httpx.Client(
                timeout=timeout_seconds
            )
        )


    def close(
        self,
    ) -> None:

        if self._owns_client:
            self.client.close()


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
                provider="ntfy",
                device_id=(
                    message.device_id
                ),
                error=(
                    "No active ntfy endpoint."
                ),
            )

        try:

            response = self.client.post(
                f"{endpoint.base_url}/",
                json={
                    "topic":
                        endpoint.topic,

                    "title":
                        message.title,

                    "message":
                        message.body,

                    "priority":
                        3,

                    "tags": [
                        "brain",
                    ],
                },
            )

            response.raise_for_status()

        except Exception as error:

            return NotificationResult(
                success=False,
                provider="ntfy",
                device_id=(
                    message.device_id
                ),
                error=str(
                    error
                ),
            )

        message_id = None

        try:

            payload = response.json()

            message_id = payload.get(
                "id"
            )

        except ValueError:
            pass

        return NotificationResult(
            success=True,
            provider="ntfy",
            device_id=(
                message.device_id
            ),
            message_id=(
                message_id
                or "ntfy-accepted"
            ),
        )
