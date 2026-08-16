from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_SESSION_ID = "default"

_SESSION_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{1,64}$"
)


def normalize_session_id(
    session_id: str | None,
) -> str:
    """
    Validate a lightweight live-channel identifier.

    Session IDs are routing identifiers, not authentication.
    """

    if session_id is None:
        return DEFAULT_SESSION_ID

    normalized = session_id.strip()

    if not _SESSION_PATTERN.fullmatch(
        normalized
    ):
        raise ValueError(
            "session_id must contain only "
            "letters, numbers, '-' or '_' "
            "and be 1-64 characters long."
        )

    return normalized


class LiveExplanationStore:
    """
    Cross-process store for Code2Plain live explanations.

    SQLite is used because the MCP server and web API may
    run in separate Python processes.

    Every explanation belongs to a session_id so independent
    live channels do not read one another's code.

    This store NEVER executes user code.
    It only persists explanation payloads.
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
        """
        Create the current schema and migrate the pre-session
        prototype database in place when necessary.
        """

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS live_explanations (
                    version INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    session_id TEXT NOT NULL DEFAULT 'default'
                )
                """
            )

            columns = {
                row["name"]
                for row
                in connection.execute(
                    """
                    PRAGMA table_info(live_explanations)
                    """
                ).fetchall()
            }

            if "session_id" not in columns:
                connection.execute(
                    """
                    ALTER TABLE live_explanations
                    ADD COLUMN session_id TEXT
                    NOT NULL DEFAULT 'default'
                    """
                )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_live_explanations_session_version
                ON live_explanations (
                    session_id,
                    version DESC
                )
                """
            )

    def publish(
        self,
        payload: dict[str, Any],
        *,
        source: str,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> int:
        session_id = normalize_session_id(
            session_id
        )

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
                    payload,
                    session_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    created_at,
                    source,
                    serialized,
                    session_id,
                ),
            )

            version = cursor.lastrowid

        if version is None:
            raise RuntimeError(
                "Live explanation version "
                "was not created."
            )

        return int(version)

    def latest(
        self,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> dict[str, Any] | None:
        session_id = normalize_session_id(
            session_id
        )

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    version,
                    created_at,
                    source,
                    payload,
                    session_id
                FROM live_explanations
                WHERE session_id = ?
                ORDER BY version DESC
                LIMIT 1
                """,
                (
                    session_id,
                ),
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
            "session_id": row[
                "session_id"
            ],
            "explanation": json.loads(
                row["payload"]
            ),
        }

    def latest_after(
        self,
        version: int,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> dict[str, Any] | None:
        latest = self.latest(
            session_id=session_id
        )

        if latest is None:
            return None

        if latest["version"] <= version:
            return None

        return latest
