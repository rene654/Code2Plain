from __future__ import annotations

import hashlib
import secrets
import sqlite3

from datetime import (
    datetime,
    timezone,
)
from pathlib import Path

from code2plain.devices.ntfy_models import (
    NtfyEndpoint,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


class NtfyEndpointRegistry:
    """
    Stores temporary/free notification endpoints.

    The ntfy topic behaves like a delivery secret and must
    be high entropy.

    It is deliberately separate from:
    - subscription entitlements
    - Apple APNs tokens
    - source code
    - phone numbers
    """

    def __init__(
        self,
        path: str | Path = "code2plain_devices.db",
    ) -> None:

        self.path = Path(
            path
        )

        self._initialize()


    def _connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            self.path
        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection


    def _initialize(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ntfy_endpoints (
                    device_id TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    topic_fingerprint TEXT NOT NULL,
                    base_url TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    revoked_at TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_ntfy_topic_fingerprint
                ON ntfy_endpoints (
                    topic_fingerprint
                )
                """
            )

            connection.commit()


    @staticmethod
    def generate_topic() -> str:

        return (
            "code2plain-"
            + secrets.token_urlsafe(
                24
            )
        )


    @staticmethod
    def _fingerprint(
        topic: str,
    ) -> str:

        return hashlib.sha256(
            topic.encode(
                "utf-8"
            )
        ).hexdigest()[:16]


    def register(
        self,
        *,
        device_id: str,
        topic: str | None = None,
        base_url: str = "https://ntfy.sh",
        now: datetime | None = None,
    ) -> NtfyEndpoint:

        device_id = (
            device_id.strip()
        )

        if not device_id:
            raise ValueError(
                "device_id cannot be empty"
            )

        topic = (
            topic
            or self.generate_topic()
        ).strip()

        if not topic:
            raise ValueError(
                "topic cannot be empty"
            )

        base_url = (
            base_url
            .strip()
            .rstrip("/")
        )

        if not base_url:
            raise ValueError(
                "base_url cannot be empty"
            )

        timestamp = (
            now
            or utc_now()
        )

        existing = self.get(
            device_id
        )

        created_at = (
            existing.created_at
            if existing
            else timestamp
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO ntfy_endpoints (
                    device_id,
                    topic,
                    topic_fingerprint,
                    base_url,
                    created_at,
                    updated_at,
                    revoked_at
                )
                VALUES (?, ?, ?, ?, ?, ?, NULL)

                ON CONFLICT(device_id)
                DO UPDATE SET
                    topic = excluded.topic,
                    topic_fingerprint =
                        excluded.topic_fingerprint,
                    base_url = excluded.base_url,
                    updated_at = excluded.updated_at,
                    revoked_at = NULL
                """,
                (
                    device_id,
                    topic,
                    self._fingerprint(
                        topic
                    ),
                    base_url,
                    created_at.isoformat(),
                    timestamp.isoformat(),
                ),
            )

            connection.commit()

        endpoint = self.get(
            device_id
        )

        if endpoint is None:
            raise RuntimeError(
                "ntfy endpoint was not persisted"
            )

        return endpoint


    def get(
        self,
        device_id: str,
    ) -> NtfyEndpoint | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    device_id,
                    topic,
                    base_url,
                    created_at,
                    updated_at,
                    revoked_at
                FROM ntfy_endpoints
                WHERE device_id = ?
                LIMIT 1
                """,
                (
                    device_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return NtfyEndpoint(
            device_id=row[
                "device_id"
            ],
            topic=row[
                "topic"
            ],
            base_url=row[
                "base_url"
            ],
            created_at=(
                datetime.fromisoformat(
                    row[
                        "created_at"
                    ]
                )
            ),
            updated_at=(
                datetime.fromisoformat(
                    row[
                        "updated_at"
                    ]
                )
            ),
            revoked_at=(
                datetime.fromisoformat(
                    row[
                        "revoked_at"
                    ]
                )
                if row[
                    "revoked_at"
                ]
                else None
            ),
        )


    def revoke(
        self,
        device_id: str,
        *,
        now: datetime | None = None,
    ) -> NtfyEndpoint:

        endpoint = self.get(
            device_id
        )

        if endpoint is None:
            raise ValueError(
                "ntfy endpoint not found"
            )

        timestamp = (
            now
            or utc_now()
        )

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE ntfy_endpoints
                SET revoked_at = ?,
                    updated_at = ?
                WHERE device_id = ?
                """,
                (
                    timestamp.isoformat(),
                    timestamp.isoformat(),
                    device_id,
                ),
            )

            connection.commit()

        updated = self.get(
            device_id
        )

        if updated is None:
            raise RuntimeError(
                "ntfy endpoint disappeared after revoke"
            )

        return updated
