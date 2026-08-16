from __future__ import annotations

from dataclasses import dataclass

from code2plain.devices.push_models import (
    ApplePushEndpoint,
)
from code2plain.devices.push_registry import (
    ApplePushRegistry,
)
from code2plain.devices.registry import (
    DeviceRegistry,
)


@dataclass(frozen=True)
class ApplePushRegistrationResult:
    device_id: str
    status: str
    endpoint: ApplePushEndpoint


class ApplePushRegistrationService:
    """
    Redeems a one-time Code2Plain pairing token and attaches
    the resulting internal device to an APNs endpoint.

    Pairing authorizes the device.

    It does not grant subscription entitlements.
    """

    def __init__(
        self,
        device_registry: DeviceRegistry,
        apple_push_registry: ApplePushRegistry,
    ) -> None:

        self.device_registry = (
            device_registry
        )

        self.apple_push_registry = (
            apple_push_registry
        )


    def register(
        self,
        *,
        pairing_token: str,
        apns_token: str,
        bundle_id: str,
        environment: str = "sandbox",
    ) -> ApplePushRegistrationResult:

        device = (
            self.device_registry
            .redeem_pairing_token(
                pairing_token
            )
        )

        endpoint = (
            self.apple_push_registry
            .register(
                device_id=(
                    device.device_id
                ),
                apns_token=(
                    apns_token
                ),
                bundle_id=(
                    bundle_id
                ),
                environment=(
                    environment
                ),
            )
        )

        return ApplePushRegistrationResult(
            device_id=(
                device.device_id
            ),
            status="connected",
            endpoint=endpoint,
        )
