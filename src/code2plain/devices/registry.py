from __future__ import annotations

import hashlib
import secrets
import sqlite3
import uuid

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from pathlib import Path

from code2plain.devices.models import (
    DeviceRecord,
    PairingRequest,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


class DeviceRegistry:
    """
    Secure pairing registry.

    Design:
    - no phone number
    - pairing tokens are one-time
    - pairing tokens expire
    - raw pairing tokens are not stored
    - devices are revocable
    """

    def __init__(
        self,
        path: str | Path = "code2plain_devices.db",
        *,
        pairing_ttl_minutes: int = 10,
    ) -> None:

        if pairing_ttl_minutes <= 0:
            raise ValueError(
                "pairing_ttl_minutes must be positive"
            )

        self.path = Path(path)

        self.pairing_ttl = timedelta(
            minutes=pairing_ttl_minutes
        )

        self._initialize()


    def _connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            self.path
        )

        connection.row_factory = sqlite3.Row

        return connection


    def _initialize(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pairing_requests (
                    pairing_id TEXT PRIMARY KEY,
                    learner_id TEXT NOT NULL,
                    token_hash TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    used_at TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS devices (
                    device_id TEXT PRIMARY KEY,
                    learner_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    revoked_at TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_devices_learner
                ON devices (
                    learner_id
                )
                """
            )

            connection.commit()


    @staticmethod
    def _hash_token(
        token: str,
    ) -> str:

        return hashlib.sha256(
            token.encode(
                "utf-8"
            )
        ).hexdigest()


    def create_pairing_request(
        self,
        learner_id: str,
        *,
        now: datetime | None = None,
    ) -> PairingRequest:

        learner_id = learner_id.strip()

        if not learner_id:
            raise ValueError(
                "learner_id cannot be empty"
            )

        timestamp = (
            now
            or utc_now()
        )

        pairing_id = (
            "pair_"
            + uuid.uuid4().hex
        )

        token = secrets.token_urlsafe(
            24
        )

        expires_at = (
            timestamp
            + self.pairing_ttl
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO pairing_requests (
                    pairing_id,
                    learner_id,
                    token_hash,
                    created_at,
                    expires_at,
                    used_at
                )
                VALUES (?, ?, ?, ?, ?, NULL)
                """,
                (
                    pairing_id,
                    learner_id,
                    self._hash_token(
                        token
                    ),
                    timestamp.isoformat(),
                    expires_at.isoformat(),
                ),
            )

            connection.commit()

        return PairingRequest(
            pairing_id=pairing_id,
            learner_id=learner_id,
            token=token,
            created_at=timestamp,
            expires_at=expires_at,
            used_at=None,
        )


    def redeem_pairing_token(
        self,
        token: str,
        *,
        now: datetime | None = None,
    ) -> DeviceRecord:

        if not token.strip():
            raise ValueError(
                "pairing token cannot be empty"
            )

        timestamp = (
            now
            or utc_now()
        )

        token_hash = self._hash_token(
            token
        )

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    pairing_id,
                    learner_id,
                    expires_at,
                    used_at
                FROM pairing_requests
                WHERE token_hash = ?
                LIMIT 1
                """,
                (
                    token_hash,
                ),
            ).fetchone()

            if row is None:
                raise ValueError(
                    "invalid pairing token"
                )

            if row["used_at"] is not None:
                raise ValueError(
                    "pairing token already used"
                )

            expires_at = (
                datetime.fromisoformat(
                    row["expires_at"]
                )
            )

            if timestamp >= expires_at:
                raise ValueError(
                    "pairing token expired"
                )

            device_id = (
                "device_"
                + uuid.uuid4().hex
            )

            connection.execute(
                """
                INSERT INTO devices (
                    device_id,
                    learner_id,
                    created_at,
                    revoked_at
                )
                VALUES (?, ?, ?, NULL)
                """,
                (
                    device_id,
                    row["learner_id"],
                    timestamp.isoformat(),
                ),
            )

            connection.execute(
                """
                UPDATE pairing_requests
                SET used_at = ?
                WHERE pairing_id = ?
                """,
                (
                    timestamp.isoformat(),
                    row["pairing_id"],
                ),
            )

            connection.commit()

        return DeviceRecord(
            device_id=device_id,
            learner_id=row["learner_id"],
            created_at=timestamp,
            revoked_at=None,
        )


    def get_device(
        self,
        device_id: str,
    ) -> DeviceRecord | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    device_id,
                    learner_id,
                    created_at,
                    revoked_at
                FROM devices
                WHERE device_id = ?
                LIMIT 1
                """,
                (
                    device_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return DeviceRecord(
            device_id=row["device_id"],
            learner_id=row["learner_id"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            revoked_at=(
                datetime.fromisoformat(
                    row["revoked_at"]
                )
                if row["revoked_at"]
                else None
            ),
        )


    def list_devices(
        self,
        learner_id: str,
    ) -> list[DeviceRecord]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    device_id,
                    learner_id,
                    created_at,
                    revoked_at
                FROM devices
                WHERE learner_id = ?
                ORDER BY created_at
                """,
                (
                    learner_id,
                ),
            ).fetchall()

        return [
            DeviceRecord(
                device_id=row["device_id"],
                learner_id=row["learner_id"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                ),
                revoked_at=(
                    datetime.fromisoformat(
                        row["revoked_at"]
                    )
                    if row["revoked_at"]
                    else None
                ),
            )
            for row in rows
        ]


    def revoke_device(
        self,
        device_id: str,
        *,
        now: datetime | None = None,
    ) -> DeviceRecord:

        timestamp = (
            now
            or utc_now()
        )

        device = self.get_device(
            device_id
        )

        if device is None:
            raise ValueError(
                "device not found"
            )

        if device.revoked_at is not None:
            return device

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE devices
                SET revoked_at = ?
                WHERE device_id = ?
                """,
                (
                    timestamp.isoformat(),
                    device_id,
                ),
            )

            connection.commit()

        updated = self.get_device(
            device_id
        )

        if updated is None:
            raise RuntimeError(
                "device disappeared after revocation"
            )

        return updated
