from __future__ import annotations

from pathlib import Path

from code2plain.devices import (
    DeviceRegistry,
    NtfyEndpointRegistry,
)


DATABASE = Path(
    "code2plain_devices.db"
)

LEARNER_ID = (
    "learner_iphone_demo"
)


device_registry = DeviceRegistry(
    DATABASE
)

ntfy_registry = NtfyEndpointRegistry(
    DATABASE
)


pairing = (
    device_registry
    .create_pairing_request(
        LEARNER_ID
    )
)


device = (
    device_registry
    .redeem_pairing_token(
        pairing.token
    )
)


endpoint = (
    ntfy_registry
    .register(
        device_id=device.device_id
    )
)


print()
print(
    "========================================"
)
print(
    " CODE2PLAIN — REAL LEARNING DEVICE"
)
print(
    "========================================"
)

print()
print(
    "Learner:"
)
print(
    LEARNER_ID
)

print()
print(
    "Device:"
)
print(
    device.device_id
)

print()
print(
    "Subscribe your iPhone to this NEW ntfy topic:"
)

print()
print(
    endpoint.topic
)

print()
print(
    "IMPORTANT:"
)
print(
    "Do not share this topic publicly."
)

print()
print(
    "After subscribing, run:"
)
print(
    "python scripts/send_learning_digest_iphone.py"
)

print()
