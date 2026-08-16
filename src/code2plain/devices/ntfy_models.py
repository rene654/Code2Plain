from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NtfyEndpoint:
    device_id: str
    topic: str
    base_url: str
    created_at: datetime
    updated_at: datetime
    revoked_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None
