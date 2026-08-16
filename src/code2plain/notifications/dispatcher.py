from __future__ import annotations

from code2plain.devices import (
    DeviceRegistry,
)
from code2plain.entitlements.service import (
    EntitlementService,
    FEATURE_MOBILE_DIGEST,
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
    Sends pedagogical notifications only when:

    1. the account is entitled to the feature
    2. the learner owns active paired devices
    3. the delivery provider accepts the message

    Pairing alone never grants Premium access.
    """

    def __init__(
        self,
        device_registry: DeviceRegistry,
        provider: NotificationProvider,
        entitlement_service: (
            EntitlementService | None
        ) = None,
    ) -> None:

        self.device_registry = (
            device_registry
        )

        self.provider = provider

        self.entitlement_service = (
            entitlement_service
        )


    def dispatch_digest(
        self,
        learner_id: str,
        digest: AdaptiveSessionDigest,
        *,
        account_id: str | None = None,
    ) -> list[NotificationResult]:

        if self.entitlement_service is not None:

            if account_id is None:
                raise ValueError(
                    "account_id is required when "
                    "entitlements are enabled"
                )

            entitlement = (
                self.entitlement_service.check(
                    account_id,
                    FEATURE_MOBILE_DIGEST,
                )
            )

            if not entitlement.allowed:
                return []

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

        if not active_devices:
            return []

        results: list[
            NotificationResult
        ] = []

        successful_delivery = False

        for device in active_devices:

            message = (
                self._build_message(
                    device.device_id,
                    digest,
                )
            )

            result = (
                self.provider.send(
                    message
                )
            )

            results.append(
                result
            )

            if result.success:
                successful_delivery = True

        if (
            successful_delivery
            and self.entitlement_service
            is not None
            and account_id
            is not None
        ):
            self.entitlement_service.consume(
                account_id,
                FEATURE_MOBILE_DIGEST,
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

        return NotificationMessage(
            device_id=device_id,
            title=(
                title_by_language.get(
                    digest.language,
                    title_by_language["es"],
                )
            ),
            body=digest.key_learning,
        )
