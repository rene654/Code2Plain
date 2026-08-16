from __future__ import annotations

import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class LiveExplanationStore:
    """
    Small cross-process store for the latest Code2Plain explanation.

    Why SQLite?
    - MCP and Web UI may run in different Python processes.
    - In-memory state would not be shared.
    - SQLite requires no additional service.
    - Later it can be replaced by Redis/Postgres without changing
      the pedagogical engine.

    This store does NOT execute user code.
    It only stores explanation payloads.
    """

    def __init__(
        self,
        path: str | Path | None = None,
    ) -> None:
        if path is None:
            configured = os.getenv(
                "CODE2PLAIN_LIVE_DB"
            )

            if configured:
                path = Path(configured)
            else:
                path = (
                    Path.cwd()
                    / ".code2plain"
                    / "live_state.db"
                )

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    def _connect(
        self,
    ) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=5,
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
                CREATE TABLE IF NOT EXISTS live_explanations (
                    version INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def publish(
        self,
        payload: dict[str, Any],
        *,
        source: str,
    ) -> int:
        created_at = (
            datetime.now(UTC)
            .isoformat()
        )

        serialized = json.dumps(
            payload,
            ensure_ascii=False,
        )

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO live_explanations (
                    created_at,
                    source,
                    payload
                )
                VALUES (?, ?, ?)
                """,
                (
                    created_at,
                    source,
                    serialized,
                ),
            )

            version = cursor.lastrowid

        if version is None:
            raise RuntimeError(
                "Live explanation version was not created."
            )

        return int(version)

    def latest(
        self,
    ) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    version,
                    created_at,
                    source,
                    payload
                FROM live_explanations
                ORDER BY version DESC
                LIMIT 1
                """
            ).fetchone()

        if row is None:
            return None

        return {
            "version": int(
                row["version"]
            ),
            "created_at": row[
                "created_at"
            ],
            "source": row["source"],
            "explanation": json.loads(
                row["payload"]
            ),
        }

    def latest_after(
        self,
        version: int,
    ) -> dict[str, Any] | None:
        latest = self.latest()

        if latest is None:
            return None

        if latest["version"] <= version:
            return None

        return latest
