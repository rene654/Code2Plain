from __future__ import annotations

from datetime import datetime

from code2plain.learning.models import (
    LearningConceptState,
    LearningProfile,
    LearningSession,
    utc_now,
)


class SessionLearningTracker:
    """
    Tracks semantic learning signals.

    Privacy rule:
    the learning profile stores concepts and exposure metadata,
    not source code.
    """

    def __init__(
        self,
        learner_id: str,
        session_id: str,
        *,
        profile: LearningProfile | None = None,
    ) -> None:

        learner_id = learner_id.strip()
        session_id = session_id.strip()

        if not learner_id:
            raise ValueError(
                "learner_id cannot be empty"
            )

        if not session_id:
            raise ValueError(
                "session_id cannot be empty"
            )

        self.profile = (
            profile
            or LearningProfile(
                learner_id=learner_id
            )
        )

        if (
            self.profile.learner_id
            != learner_id
        ):
            raise ValueError(
                "profile learner_id does not match"
            )

        self.session = LearningSession(
            session_id=session_id,
            learner_id=learner_id,
        )


    def observe_explanation(
        self,
        explanation: dict,
        *,
        observed_at: datetime | None = None,
    ) -> LearningSession:

        if self.session.is_closed:
            raise RuntimeError(
                "learning session is already closed"
            )

        timestamp = (
            observed_at
            or utc_now()
        )

        sections = (
            explanation.get(
                "sections",
                [],
            )
            or []
        )

        concepts: list[str] = []

        for section in sections:
            concept = (
                section.get(
                    "concept"
                )
                or ""
            ).strip()

            if (
                not concept
                or concept in concepts
            ):
                continue

            concepts.append(
                concept
            )

        self.session.explanation_count += 1
        self.session.last_activity_at = timestamp

        for concept in concepts:
            self._observe_concept(
                concept,
                timestamp,
            )

        return self.session


    def _observe_concept(
        self,
        concept: str,
        timestamp: datetime,
    ) -> None:

        state = (
            self.profile
            .concepts
            .get(
                concept
            )
        )

        if state is None:
            state = LearningConceptState(
                concept=concept,
                first_seen_at=timestamp,
                last_seen_at=timestamp,
            )

            self.profile.concepts[
                concept
            ] = state

            self.session.new_concepts.append(
                concept
            )

        state.total_exposures += 1
        state.session_exposures += 1
        state.last_seen_at = timestamp

        state.status = (
            self._classify_status(
                state.total_exposures
            )
        )

        self.session.concept_counts[
            concept
        ] = (
            self.session
            .concept_counts
            .get(
                concept,
                0,
            )
            + 1
        )


    @staticmethod
    def _classify_status(
        total_exposures: int,
    ) -> str:

        if total_exposures <= 1:
            return "new"

        if total_exposures <= 4:
            return "practicing"

        return "familiar"


    def close_session(
        self,
        *,
        ended_at: datetime | None = None,
    ) -> LearningSession:

        if self.session.is_closed:
            return self.session

        self.session.ended_at = (
            ended_at
            or utc_now()
        )

        return self.session
