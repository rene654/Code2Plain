from datetime import (
    datetime,
    timezone,
)

from code2plain.learning import (
    LearningProfileStore,
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


def test_profile_can_be_saved_and_loaded(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
            "AGGREGATE",
        )
    )

    store.save(
        tracker.profile
    )

    loaded = store.load(
        "learner_1"
    )

    assert (
        loaded.concepts[
            "FILTER"
        ].total_exposures
        == 1
    )

    assert (
        loaded.concepts[
            "AGGREGATE"
        ].status
        == "new"
    )


def test_profile_survives_new_tracker(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    first = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    first.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    store.save(
        first.profile
    )

    loaded = store.load(
        "learner_1"
    )

    second = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_2",
        profile=loaded,
    )

    second.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    assert (
        second.profile.concepts[
            "FILTER"
        ].total_exposures
        == 2
    )

    assert (
        second.profile.concepts[
            "FILTER"
        ].status
        == "practicing"
    )


def test_profile_exists(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    assert (
        not store.exists(
            "learner_1"
        )
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    store.save(
        tracker.profile
    )

    assert (
        store.exists(
            "learner_1"
        )
    )


def test_profile_can_be_deleted(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    store.save(
        tracker.profile
    )

    store.delete(
        "learner_1"
    )

    assert (
        not store.exists(
            "learner_1"
        )
    )

    assert (
        store.load(
            "learner_1"
        ).concepts
        == {}
    )


def test_timestamps_survive_round_trip(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    moment = datetime(
        2026,
        8,
        16,
        15,
        30,
        tzinfo=timezone.utc,
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        ),
        observed_at=moment,
    )

    store.save(
        tracker.profile
    )

    loaded = store.load(
        "learner_1"
    )

    assert (
        loaded.concepts[
            "FILTER"
        ].first_seen_at
        == moment
    )

    assert (
        loaded.concepts[
            "FILTER"
        ].last_seen_at
        == moment
    )


def test_session_exposures_are_not_persisted(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    assert (
        tracker.profile.concepts[
            "FILTER"
        ].session_exposures
        == 1
    )

    store.save(
        tracker.profile
    )

    loaded = store.load(
        "learner_1"
    )

    assert (
        loaded.concepts[
            "FILTER"
        ].session_exposures
        == 0
    )


def test_profile_export_contains_learning_data_only(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    store.save(
        tracker.profile
    )

    exported = store.export_profile(
        "learner_1"
    )

    serialized = str(
        exported
    ).lower()

    assert (
        "filter"
        in serialized
    )

    assert (
        "phone"
        not in serialized
    )

    assert (
        "push_token"
        not in serialized
    )

    assert (
        "source_code"
        not in serialized
    )
