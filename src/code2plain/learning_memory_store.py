import sqlite3
from pathlib import Path


class LearningMemoryStore:
    def __init__(
        self,
        path: str | Path = ".code2plain/learning_memory.db",
    ) -> None:
        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._init_db()

    def _connect(self):
        return sqlite3.connect(
            self.path
        )

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS concept_progress (
                    concept TEXT PRIMARY KEY,
                    seen INTEGER NOT NULL DEFAULT 0,
                    correct INTEGER NOT NULL DEFAULT 0,
                    incorrect INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    def record_seen(
        self,
        concept: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO concept_progress (
                    concept,
                    seen
                )
                VALUES (?, 1)
                ON CONFLICT(concept)
                DO UPDATE SET
                    seen = seen + 1
                """,
                (concept,),
            )

    def record_answer(
        self,
        concept: str,
        *,
        correct: bool,
    ) -> None:
        field = (
            "correct"
            if correct
            else "incorrect"
        )

        with self._connect() as connection:
            connection.execute(
                f"""
                INSERT INTO concept_progress (
                    concept,
                    {field}
                )
                VALUES (?, 1)
                ON CONFLICT(concept)
                DO UPDATE SET
                    {field} = {field} + 1
                """,
                (concept,),
            )

    def get(
        self,
        concept: str,
    ) -> dict:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    seen,
                    correct,
                    incorrect
                FROM concept_progress
                WHERE concept = ?
                """,
                (concept,),
            ).fetchone()

        if row is None:
            return {
                "seen": 0,
                "correct": 0,
                "incorrect": 0,
            }

        return {
            "seen": row[0],
            "correct": row[1],
            "incorrect": row[2],
        }


learning_memory_store = LearningMemoryStore()
