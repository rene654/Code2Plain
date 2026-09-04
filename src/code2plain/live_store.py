from __future__ import annotations

import re
import threading
from datetime import UTC, datetime, timedelta
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
    Ephemeral live-learning channel.

    Privacy rule:
    - source code and explanation payloads stay in RAM only
    - nothing from this channel is written to SQLite or disk
    - persistent learning memory is handled separately and
      stores abstract concepts/progress only

    The optional path argument remains only for backwards
    compatibility with existing callers/tests. It is ignored.
    """

    def __init__(
        self,
        path: str | Path | None = None,
        *,
        ttl_seconds: int = 900,
        max_sessions: int = 1000,
    ) -> None:
        self.path = None

        self.ttl = timedelta(
            seconds=ttl_seconds
        )

        if max_sessions < 1:
            raise ValueError(
                "max_sessions must be at least 1."
            )

        self.max_sessions = (
            max_sessions
        )

        self._lock = threading.Lock()

        self._version = 0

        self._latest_by_session: dict[
            str,
            dict[str, Any],
        ] = {}

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

        created_at = datetime.now(UTC)

        with self._lock:
            self._purge_expired_locked(
                created_at
            )

            if (
                session_id
                not in self._latest_by_session
                and len(
                    self._latest_by_session
                ) >= self.max_sessions
            ):
                self._evict_oldest_locked()

            self._version += 1

            version = self._version

            self._latest_by_session[
                session_id
            ] = {
                "version": version,
                "created_at":
                    created_at.isoformat(),
                "created_at_dt":
                    created_at,
                "source": source,
                "session_id":
                    session_id,
                "explanation":
                    payload,
            }

        return version

    def latest(
        self,
        session_id: str = DEFAULT_SESSION_ID,
    ) -> dict[str, Any] | None:
        session_id = normalize_session_id(
            session_id
        )

        now = datetime.now(UTC)

        with self._lock:
            self._purge_expired_locked(
                now
            )

            item = (
                self._latest_by_session
                .get(session_id)
            )

            if item is None:
                return None

            return {
                "version":
                    item["version"],
                "created_at":
                    item["created_at"],
                "source":
                    item["source"],
                "session_id":
                    item["session_id"],
                "explanation":
                    item["explanation"],
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

    def clear(
        self,
        session_id: str | None = None,
    ) -> None:
        with self._lock:
            if session_id is None:
                self._latest_by_session.clear()
                return

            normalized = (
                normalize_session_id(
                    session_id
                )
            )

            self._latest_by_session.pop(
                normalized,
                None,
            )

    def _evict_oldest_locked(
        self,
    ) -> None:
        if not self._latest_by_session:
            return

        oldest_session = min(
            self._latest_by_session,
            key=lambda session_id: (
                self._latest_by_session[
                    session_id
                ]["created_at_dt"]
            ),
        )

        self._latest_by_session.pop(
            oldest_session,
            None,
        )


    def _purge_expired_locked(
        self,
        now: datetime,
    ) -> None:
        expired = [
            session_id
            for session_id, item
            in self._latest_by_session.items()
            if (
                now
                - item["created_at_dt"]
                > self.ttl
            )
        ]

        for session_id in expired:
            self._latest_by_session.pop(
                session_id,
                None,
            )


# Shared process-wide ephemeral channel.
#
# Production deployment mounts MCP + API in the same process,
# so this channel does not require persistent storage.
live_store = LiveExplanationStore()
