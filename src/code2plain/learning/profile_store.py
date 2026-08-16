from __future__ import annotations

import json
import sqlite3

from datetime import datetime
from pathlib import Path

from code2plain.learning.models import (
    LearningConceptState,
    LearningProfile,
)


class LearningProfileStore:
    """
    SQLite-backed persistence for pedagogical state.

    Privacy rule:
    this store persists learning metadata only.
    It does not persist source code, phone numbers,
    device identifiers, or push tokens.
    """

    def __init__(
        self,
        path: str | Path = "code2plain_learning.db",
    ) -> None:

        self.path = Path(path)

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
                CREATE TABLE IF NOT EXISTS
                learning_profiles (
                    learner_id TEXT PRIMARY KEY,
                    updated_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS
                learning_concepts (
                    learner_id TEXT NOT NULL,
                    concept TEXT NOT NULL,
                    total_exposures INTEGER NOT NULL,
                    first_seen_at TEXT,
                    last_seen_at TEXT,
                    status TEXT NOT NULL,
                    PRIMARY KEY (
                        learner_id,
                        concept
                    )
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_learning_concepts_learner
                ON learning_concepts (
                    learner_id
                )
                """
            )

            connection.commit()


    def save(
        self,
        profile: LearningProfile,
    ) -> None:

        if not profile.learner_id.strip():
            raise ValueError(
                "learner_id cannot be empty"
            )

        updated_at = (
            datetime
            .now()
            .astimezone()
            .isoformat()
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO learning_profiles (
                    learner_id,
                    updated_at
                )
                VALUES (?, ?)
                ON CONFLICT(learner_id)
                DO UPDATE SET
                    updated_at = excluded.updated_at
                """,
                (
                    profile.learner_id,
                    updated_at,
                ),
            )

            connection.execute(
                """
                DELETE FROM learning_concepts
                WHERE learner_id = ?
                """,
                (
                    profile.learner_id,
                ),
            )

            for state in (
                profile
                .concepts
                .values()
            ):

                connection.execute(
                    """
                    INSERT INTO learning_concepts (
                        learner_id,
                        concept,
                        total_exposures,
                        first_seen_at,
                        last_seen_at,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        profile.learner_id,
                        state.concept,
                        state.total_exposures,
                        (
                            state.first_seen_at
                            .isoformat()
                            if state.first_seen_at
                            else None
                        ),
                        (
                            state.last_seen_at
                            .isoformat()
                            if state.last_seen_at
                            else None
                        ),
                        state.status,
                    ),
                )

            connection.commit()


    def load(
        self,
        learner_id: str,
    ) -> LearningProfile:

        learner_id = (
            learner_id.strip()
        )

        if not learner_id:
            raise ValueError(
                "learner_id cannot be empty"
            )

        profile = LearningProfile(
            learner_id=learner_id
        )

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    concept,
                    total_exposures,
                    first_seen_at,
                    last_seen_at,
                    status
                FROM learning_concepts
                WHERE learner_id = ?
                ORDER BY concept
                """,
                (
                    learner_id,
                ),
            ).fetchall()

        for row in rows:

            profile.concepts[
                row["concept"]
            ] = LearningConceptState(
                concept=row["concept"],
                total_exposures=(
                    row[
                        "total_exposures"
                    ]
                ),
                session_exposures=0,
                first_seen_at=(
                    datetime.fromisoformat(
                        row[
                            "first_seen_at"
                        ]
                    )
                    if row[
                        "first_seen_at"
                    ]
                    else None
                ),
                last_seen_at=(
                    datetime.fromisoformat(
                        row[
                            "last_seen_at"
                        ]
                    )
                    if row[
                        "last_seen_at"
                    ]
                    else None
                ),
                status=row["status"],
            )

        return profile


    def exists(
        self,
        learner_id: str,
    ) -> bool:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT 1
                FROM learning_profiles
                WHERE learner_id = ?
                LIMIT 1
                """,
                (
                    learner_id,
                ),
            ).fetchone()

        return row is not None


    def delete(
        self,
        learner_id: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM learning_concepts
                WHERE learner_id = ?
                """,
                (
                    learner_id,
                ),
            )

            connection.execute(
                """
                DELETE FROM learning_profiles
                WHERE learner_id = ?
                """,
                (
                    learner_id,
                ),
            )

            connection.commit()


    def export_profile(
        self,
        learner_id: str,
    ) -> dict:

        profile = self.load(
            learner_id
        )

        return {
            "learner_id":
                profile.learner_id,

            "concepts": {
                concept: {
                    "total_exposures":
                        state.total_exposures,

                    "first_seen_at":
                        (
                            state.first_seen_at
                            .isoformat()
                            if state.first_seen_at
                            else None
                        ),

                    "last_seen_at":
                        (
                            state.last_seen_at
                            .isoformat()
                            if state.last_seen_at
                            else None
                        ),

                    "status":
                        state.status,
                }

                for concept, state
                in profile.concepts.items()
            },
        }


    def export_json(
        self,
        learner_id: str,
    ) -> str:

        return json.dumps(
            self.export_profile(
                learner_id
            ),
            ensure_ascii=False,
            indent=2,
        )
