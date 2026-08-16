from datetime import (
    datetime,
    timezone,
)

import pytest

from code2plain.learning import (
    LearningProfile,
    SessionLearningTracker,
)


def explanation(
    *concepts: str,
) -> dict:
    return {
        "sections": [
            {
                "concept": concept,
            }
            for concept in concepts
        ]
    }


def test_tracker_records_concepts():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "IMPORT",
            "LOAD DATA",
            "FILTER",
        )
    )

    assert (
        tracker.session.concept_counts[
            "FILTER"
        ]
        == 1
    )


def test_tracker_deduplicates_within_one_explanation():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
            "FILTER",
        )
    )

    assert (
        tracker.session.concept_counts[
            "FILTER"
        ]
        == 1
    )


def test_first_exposure_is_new():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "AGGREGATE",
        )
    )

    assert (
        tracker.profile.concepts[
            "AGGREGATE"
        ].status
        == "new"
    )


def test_repeated_exposure_becomes_practicing():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    assert (
        tracker.profile.concepts[
            "FILTER"
        ].status
        == "practicing"
    )


def test_five_exposures_becomes_familiar():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    for _ in range(5):
        tracker.observe_explanation(
            explanation(
                "FILTER",
            )
        )

    assert (
        tracker.profile.concepts[
            "FILTER"
        ].status
        == "familiar"
    )


def test_existing_profile_is_reused():
    profile = LearningProfile(
        learner_id="learner_1"
    )

    first = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
        profile=profile,
    )

    first.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    second = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_2",
        profile=profile,
    )

    second.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    assert (
        profile.concepts[
            "FILTER"
        ].total_exposures
        == 2
    )


def test_closed_session_rejects_activity():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.close_session()

    with pytest.raises(
        RuntimeError
    ):
        tracker.observe_explanation(
            explanation(
                "FILTER",
            )
        )


def test_observed_timestamp_can_be_supplied():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    moment = datetime(
        2026,
        8,
        16,
        12,
        0,
        tzinfo=timezone.utc,
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        ),
        observed_at=moment,
    )

    assert (
        tracker.session.last_activity_at
        == moment
    )
