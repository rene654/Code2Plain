from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from code2plain.human_skills import (
    get_human_skill,
)


@dataclass(frozen=True)
class HumanSkillProgress:
    user_id: str
    skill_id: str
    seen: int
    correct: int
    incorrect: int
    mastery: float
    last_seen: str


class HumanSkillMemoryStore:
    """
    Persistent learning memory.

    Stores only abstract skill progress per user.
    Source code, snippets and explanations are not stored.
    """

    def __init__(
        self,
        path: str | Path = (
            ".code2plain/"
            "human_skill_memory.db"
        ),
    ) -> None:
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
                CREATE TABLE IF NOT EXISTS
                human_skill_progress (
                    user_id TEXT NOT NULL,
                    skill_id TEXT NOT NULL,
                    seen INTEGER NOT NULL DEFAULT 0,
                    correct INTEGER NOT NULL DEFAULT 0,
                    incorrect INTEGER NOT NULL DEFAULT 0,
                    mastery REAL NOT NULL DEFAULT 0,
                    last_seen TEXT NOT NULL,
                    PRIMARY KEY (
                        user_id,
                        skill_id
                    )
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_skill_progress_user
                ON human_skill_progress (
                    user_id
                )
                """
            )

    def record_seen(
        self,
        *,
        user_id: str,
        skill_id: str,
    ) -> HumanSkillProgress:
        self._validate(
            user_id=user_id,
            skill_id=skill_id,
        )

        now = datetime.now(UTC).isoformat()

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO human_skill_progress (
                    user_id,
                    skill_id,
                    seen,
                    correct,
                    incorrect,
                    mastery,
                    last_seen
                )
                VALUES (?, ?, 1, 0, 0, 0, ?)
                ON CONFLICT (
                    user_id,
                    skill_id
                )
                DO UPDATE SET
                    seen = seen + 1,
                    last_seen = excluded.last_seen
                """,
                (
                    user_id,
                    skill_id,
                    now,
                ),
            )

        return self.get(
            user_id=user_id,
            skill_id=skill_id,
        )

    def record_answer(
        self,
        *,
        user_id: str,
        skill_id: str,
        correct: bool,
    ) -> HumanSkillProgress:
        self._validate(
            user_id=user_id,
            skill_id=skill_id,
        )

        progress = self.record_seen(
            user_id=user_id,
            skill_id=skill_id,
        )

        new_correct = (
            progress.correct
            + (1 if correct else 0)
        )

        new_incorrect = (
            progress.incorrect
            + (0 if correct else 1)
        )

        attempts = (
            new_correct
            + new_incorrect
        )

        mastery = (
            new_correct / attempts
            if attempts
            else 0.0
        )

        now = datetime.now(UTC).isoformat()

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE human_skill_progress
                SET
                    correct = ?,
                    incorrect = ?,
                    mastery = ?,
                    last_seen = ?
                WHERE
                    user_id = ?
                    AND skill_id = ?
                """,
                (
                    new_correct,
                    new_incorrect,
                    mastery,
                    now,
                    user_id,
                    skill_id,
                ),
            )

        return self.get(
            user_id=user_id,
            skill_id=skill_id,
        )

    def get(
        self,
        *,
        user_id: str,
        skill_id: str,
    ) -> HumanSkillProgress:
        self._validate(
            user_id=user_id,
            skill_id=skill_id,
        )

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    user_id,
                    skill_id,
                    seen,
                    correct,
                    incorrect,
                    mastery,
                    last_seen
                FROM human_skill_progress
                WHERE
                    user_id = ?
                    AND skill_id = ?
                """,
                (
                    user_id,
                    skill_id,
                ),
            ).fetchone()

        if row is None:
            return HumanSkillProgress(
                user_id=user_id,
                skill_id=skill_id,
                seen=0,
                correct=0,
                incorrect=0,
                mastery=0.0,
                last_seen="",
            )

        return HumanSkillProgress(
            user_id=row["user_id"],
            skill_id=row["skill_id"],
            seen=row["seen"],
            correct=row["correct"],
            incorrect=row["incorrect"],
            mastery=row["mastery"],
            last_seen=row["last_seen"],
        )

    def list_user_skills(
        self,
        *,
        user_id: str,
    ) -> list[HumanSkillProgress]:
        if not user_id.strip():
            raise ValueError(
                "user_id cannot be empty."
            )

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    user_id,
                    skill_id,
                    seen,
                    correct,
                    incorrect,
                    mastery,
                    last_seen
                FROM human_skill_progress
                WHERE user_id = ?
                ORDER BY last_seen DESC
                """,
                (user_id,),
            ).fetchall()

        return [
            HumanSkillProgress(
                user_id=row["user_id"],
                skill_id=row["skill_id"],
                seen=row["seen"],
                correct=row["correct"],
                incorrect=row["incorrect"],
                mastery=row["mastery"],
                last_seen=row["last_seen"],
            )
            for row in rows
        ]

    def _validate(
        self,
        *,
        user_id: str,
        skill_id: str,
    ) -> None:
        if not user_id.strip():
            raise ValueError(
                "user_id cannot be empty."
            )

        if len(user_id) > 128:
            raise ValueError(
                "user_id is too long."
            )

        if get_human_skill(
            skill_id
        ) is None:
            raise ValueError(
                "Unknown human skill."
            )


human_skill_memory = HumanSkillMemoryStore()
