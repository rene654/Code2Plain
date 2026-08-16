from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationMessage:
    device_id: str
    title: str
    body: str
    digest_id: str | None = None


@dataclass(frozen=True)
class NotificationResult:
    success: bool
    provider: str
    device_id: str
    message_id: str | None = None
    error: str | None = None
