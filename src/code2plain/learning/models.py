from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


@dataclass
class LearningConceptState:
    concept: str

    total_exposures: int = 0

    session_exposures: int = 0

    first_seen_at: datetime | None = None

    last_seen_at: datetime | None = None

    status: str = "new"


@dataclass
class LearningProfile:
    learner_id: str

    concepts: dict[
        str,
        LearningConceptState,
    ] = field(
        default_factory=dict
    )


@dataclass
class LearningSession:
    session_id: str

    learner_id: str

    started_at: datetime = field(
        default_factory=utc_now
    )

    last_activity_at: datetime = field(
        default_factory=utc_now
    )

    ended_at: datetime | None = None

    explanation_count: int = 0

    concept_counts: dict[
        str,
        int,
    ] = field(
        default_factory=dict
    )

    new_concepts: list[str] = field(
        default_factory=list
    )

    @property
    def is_closed(self) -> bool:
        return (
            self.ended_at
            is not None
        )
