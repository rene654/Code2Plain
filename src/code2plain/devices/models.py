from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PairingRequest:
    pairing_id: str
    learner_id: str
    token: str
    created_at: datetime
    expires_at: datetime
    used_at: datetime | None = None


@dataclass(frozen=True)
class DeviceRecord:
    device_id: str
    learner_id: str
    created_at: datetime
    revoked_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None
