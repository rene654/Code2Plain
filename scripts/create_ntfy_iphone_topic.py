from __future__ import annotations

from pathlib import Path

from code2plain.devices import (
    NtfyEndpointRegistry,
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


endpoint = registry.register(
    device_id=DEVICE_ID
)


print()
print(
    "========================================"
)

print(
    " CODE2PLAIN — FREE iPHONE TOPIC"
)

print(
    "========================================"
)

print()

print(
    "Device ID:"
)

print(
    DEVICE_ID
)

print()

print(
    "Subscribe to this topic in the ntfy iPhone app:"
)

print()

print(
    endpoint.topic
)

print()

print(
    "Do not share this topic publicly."
)

print(
    "It behaves like a temporary delivery secret."
)

print()
