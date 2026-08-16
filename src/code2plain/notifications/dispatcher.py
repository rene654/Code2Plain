from __future__ import annotations

from code2plain.devices import (
    DeviceRegistry,
)
from code2plain.learning.adaptive_digest import (
    AdaptiveSessionDigest,
)
from code2plain.notifications.models import (
    NotificationMessage,
    NotificationResult,
)
from code2plain.notifications.provider import (
    NotificationProvider,
)


class NotificationDispatcher:
    """
    Sends pedagogical notifications only to active devices.

    Privacy:
    source code is never required for notification delivery.
    """

    def __init__(
        self,
        device_registry: DeviceRegistry,
        provider: NotificationProvider,
    ) -> None:

        self.device_registry = (
            device_registry
        )

        self.provider = provider


    def dispatch_digest(
        self,
        learner_id: str,
        digest: AdaptiveSessionDigest,
    ) -> list[NotificationResult]:

        devices = (
            self.device_registry
            .list_devices(
                learner_id
            )
        )

        active_devices = [
            device
            for device
            in devices
            if device.is_active
        ]

        results: list[
            NotificationResult
        ] = []

        for device in active_devices:

            message = (
                self._build_message(
                    device.device_id,
                    digest,
                )
            )

            results.append(
                self.provider.send(
                    message
                )
            )

        return results


    @staticmethod
    def _build_message(
        device_id: str,
        digest: AdaptiveSessionDigest,
    ) -> NotificationMessage:

        title_by_language = {
            "es":
                "Code2Plain · Sesión completada",

            "en":
                "Code2Plain · Session complete",

            "fr":
                "Code2Plain · Session terminée",
        }

        body = (
            digest.key_learning
        )

        return NotificationMessage(
            device_id=device_id,
            title=(
                title_by_language.get(
                    digest.language,
                    title_by_language["es"],
                )
            ),
            body=body,
        )
