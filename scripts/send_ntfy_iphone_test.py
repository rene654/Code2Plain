from __future__ import annotations

from pathlib import Path

from code2plain.devices import (
    NtfyEndpointRegistry,
)
from code2plain.notifications import (
    NotificationMessage,
    NtfyNotificationProvider,
)


DATABASE = Path(
    "code2plain_devices.db"
)


DEVICE_ID = (
    "device_iphone_free_demo"
)


registry = NtfyEndpointRegistry(
    DATABASE
)


endpoint = registry.get(
    DEVICE_ID
)


if (
    endpoint is None
    or not endpoint.is_active
):
    raise SystemExit(
        "No active free iPhone endpoint. "
        "Run create_ntfy_iphone_topic.py first."
    )


provider = NtfyNotificationProvider(
    registry
)


result = provider.send(
    NotificationMessage(
        device_id=DEVICE_ID,
        title=(
            "Code2Plain · "
            "Sesión completada"
        ),
        body=(
            "Prueba real: "
            "Code2Plain ya puede "
            "llegar a tu iPhone."
        ),
    )
)


provider.close()


print()

print(
    "Provider:",
    result.provider
)

print(
    "Success:",
    result.success
)

print(
    "Message ID:",
    result.message_id
)

if result.error:
    print(
        "Error:",
        result.error
    )


if not result.success:
    raise SystemExit(
        1
    )


print()

print(
    "Physical notification request: PASS"
)

print()
