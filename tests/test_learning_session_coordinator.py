from datetime import (
    datetime,
    timedelta,
    timezone,
)

from code2plain.learning import (
    AutomaticSessionEndDetector,
    LearningProfileStore,
    LearningSessionCoordinator,
    SessionLearningTracker,
)


BASE = datetime(
    2026,
    8,
    16,
    12,
    0,
    tzinfo=timezone.utc,
)


def make_tracker():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        {
            "sections": [
                {
                    "concept":
                        "FILTER"
                },
                {
                    "concept":
                        "AGGREGATE"
                },
            ]
        },
        observed_at=BASE,
    )

    return tracker


def test_coordinator_does_nothing_while_active(
    tmp_path,
):
    tracker = make_tracker()

    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    coordinator = LearningSessionCoordinator(
        tracker,
        store,
        detector=(
            AutomaticSessionEndDetector(
                idle_after_minutes=20,
                grace_minutes=5,
            )
        ),
    )

    result = coordinator.check(
        now=(
            BASE
            + timedelta(
                minutes=10
            )
        )
    )

    assert result.decision.state == "ACTIVE"
    assert result.digest is None
    assert not store.exists("learner_1")


def test_coordinator_auto_closes_and_builds_digest(
    tmp_path,
):
    tracker = make_tracker()

    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    coordinator = LearningSessionCoordinator(
        tracker,
        store,
        language="es",
        detector=(
            AutomaticSessionEndDetector(
                idle_after_minutes=20,
                grace_minutes=5,
            )
        ),
    )

    result = coordinator.check(
        now=(
            BASE
            + timedelta(
                minutes=30
            )
        )
    )

    assert result.decision.state == "CLOSED"
    assert result.digest is not None

    assert (
        "filtros"
        in result.digest.key_learning
    )

    assert store.exists(
        "learner_1"
    )


def test_digest_is_not_rebuilt_multiple_times(
    tmp_path,
):
    tracker = make_tracker()

    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    coordinator = LearningSessionCoordinator(
        tracker,
        store,
        detector=(
            AutomaticSessionEndDetector(
                idle_after_minutes=20,
                grace_minutes=5,
            )
        ),
    )

    first = coordinator.check(
        now=(
            BASE
            + timedelta(
                minutes=30
            )
        )
    )

    second = coordinator.check(
        now=(
            BASE
            + timedelta(
                minutes=40
            )
        )
    )

    assert first.digest is second.digest


def test_profile_is_persisted_automatically(
    tmp_path,
):
    tracker = make_tracker()

    store = LearningProfileStore(
        tmp_path / "learning.db"
    )

    coordinator = LearningSessionCoordinator(
        tracker,
        store,
        detector=(
            AutomaticSessionEndDetector(
                idle_after_minutes=20,
                grace_minutes=5,
            )
        ),
    )

    coordinator.check(
        now=(
            BASE
            + timedelta(
                minutes=30
            )
        )
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
