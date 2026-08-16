from __future__ import annotations

import hashlib
import sqlite3

from datetime import (
    datetime,
    timezone,
)
from pathlib import Path

from code2plain.devices.push_models import (
    ApplePushEndpoint,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


class ApplePushRegistry:
    """
    Stores Apple push endpoint metadata.

    v1.1 design:
    - no phone number
    - no source code
    - endpoint belongs to an internal device_id
    - raw APNs token is not exposed through logs
    - endpoint can be revoked

    NOTE:
    Production encryption-at-rest is handled in the
    final security/release gate. This phase establishes
    the separation and lifecycle contract.
    """

    def __init__(
        self,
        path: str | Path = "code2plain_devices.db",
    ) -> None:

        self.path = Path(path)

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
                CREATE TABLE IF NOT EXISTS apple_push_endpoints (
                    device_id TEXT PRIMARY KEY,
                    apns_token TEXT NOT NULL,
                    token_fingerprint TEXT NOT NULL,
                    bundle_id TEXT NOT NULL,
                    environment TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    revoked_at TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_apple_push_bundle
                ON apple_push_endpoints (
                    bundle_id
                )
                """
            )

            connection.commit()


    @staticmethod
    def _fingerprint(
        token: str,
    ) -> str:

        return hashlib.sha256(
            token.encode(
                "utf-8"
            )
        ).hexdigest()[:16]


    def register(
        self,
        *,
        device_id: str,
        apns_token: str,
        bundle_id: str,
        environment: str = "sandbox",
        now: datetime | None = None,
    ) -> ApplePushEndpoint:

        device_id = device_id.strip()
        apns_token = apns_token.strip()
        bundle_id = bundle_id.strip()
        environment = environment.strip()

        if not device_id:
            raise ValueError(
                "device_id cannot be empty"
            )

        if not apns_token:
            raise ValueError(
                "apns_token cannot be empty"
            )

        if not bundle_id:
            raise ValueError(
                "bundle_id cannot be empty"
            )

        if environment not in {
            "sandbox",
            "production",
        }:
            raise ValueError(
                "environment must be sandbox or production"
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
                INSERT INTO apple_push_endpoints (
                    device_id,
                    apns_token,
                    token_fingerprint,
                    bundle_id,
                    environment,
                    created_at,
                    updated_at,
                    revoked_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, NULL)

                ON CONFLICT(device_id)
                DO UPDATE SET
                    apns_token = excluded.apns_token,
                    token_fingerprint = excluded.token_fingerprint,
                    bundle_id = excluded.bundle_id,
                    environment = excluded.environment,
                    updated_at = excluded.updated_at,
                    revoked_at = NULL
                """,
                (
                    device_id,
                    apns_token,
                    self._fingerprint(
                        apns_token
                    ),
                    bundle_id,
                    environment,
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
                "endpoint was not persisted"
            )

        return endpoint


    def get(
        self,
        device_id: str,
    ) -> ApplePushEndpoint | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    device_id,
                    apns_token,
                    bundle_id,
                    environment,
                    created_at,
                    updated_at,
                    revoked_at
                FROM apple_push_endpoints
                WHERE device_id = ?
                LIMIT 1
                """,
                (
                    device_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return ApplePushEndpoint(
            device_id=row["device_id"],
            apns_token=row["apns_token"],
            bundle_id=row["bundle_id"],
            environment=row["environment"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
            revoked_at=(
                datetime.fromisoformat(
                    row["revoked_at"]
                )
                if row["revoked_at"]
                else None
            ),
        )


    def revoke(
        self,
        device_id: str,
        *,
        now: datetime | None = None,
    ) -> ApplePushEndpoint:

        timestamp = (
            now
            or utc_now()
        )

        endpoint = self.get(
            device_id
        )

        if endpoint is None:
            raise ValueError(
                "push endpoint not found"
            )

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE apple_push_endpoints
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
                "endpoint disappeared after revoke"
            )

        return updated
