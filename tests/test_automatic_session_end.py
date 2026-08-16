from datetime import (
    datetime,
    timedelta,
    timezone,
)

from code2plain.learning import (
    AutomaticSessionEndDetector,
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

    tracker.session.started_at = BASE
    tracker.session.last_activity_at = BASE

    return tracker


def test_recent_activity_stays_active():
    tracker = make_tracker()

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                minutes=10
            )
        ),
    )

    assert decision.state == "ACTIVE"
    assert not decision.should_close


def test_idle_threshold_enters_idle_state():
    tracker = make_tracker()

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                minutes=21
            )
        ),
    )

    assert decision.state == "IDLE"
    assert not decision.should_close


def test_grace_period_prevents_early_close():
    tracker = make_tracker()

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                minutes=24
            )
        ),
    )

    assert decision.state == "IDLE"
    assert not decision.should_close


def test_session_is_ready_after_full_threshold():
    tracker = make_tracker()

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                minutes=25
            )
        ),
    )

    assert (
        decision.state
        == "READY_TO_CLOSE"
    )

    assert decision.should_close


def test_auto_close_sets_ended_at():
    tracker = make_tracker()

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    now = (
        BASE
        + timedelta(
            minutes=30
        )
    )

    decision = detector.auto_close(
        tracker.session,
        now=now,
    )

    assert decision.state == "CLOSED"
    assert tracker.session.ended_at == now


def test_new_activity_resets_idle_clock():
    tracker = make_tracker()

    tracker.observe_explanation(
        {
            "sections": [
                {
                    "concept": "FILTER"
                }
            ]
        },
        observed_at=(
            BASE
            + timedelta(
                minutes=22
            )
        ),
    )

    detector = AutomaticSessionEndDetector(
        idle_after_minutes=20,
        grace_minutes=5,
    )

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                minutes=30
            )
        ),
    )

    assert decision.state == "ACTIVE"


def test_closed_session_stays_closed():
    tracker = make_tracker()

    tracker.close_session(
        ended_at=BASE
    )

    detector = AutomaticSessionEndDetector()

    decision = detector.evaluate(
        tracker.session,
        now=(
            BASE
            + timedelta(
                hours=1
            )
        ),
    )

    assert decision.state == "CLOSED"
    assert not decision.should_close
