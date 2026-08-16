import pytest

from code2plain.learning import (
    SessionDigestBuilder,
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


def make_tracker():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "IMPORT",
            "LOAD DATA",
            "FILTER",
            "AGGREGATE",
            "EXPORT",
        )
    )

    return tracker


def test_spanish_digest():
    tracker = make_tracker()

    digest = SessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        "Trabajaste con"
        in digest.summary
    )

    assert (
        "filtros"
        in digest.summary
    )

    assert digest.concept_count == 5


def test_english_digest():
    tracker = make_tracker()

    digest = SessionDigestBuilder(
        "en"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        "You worked with"
        in digest.summary
    )


def test_french_digest():
    tracker = make_tracker()

    digest = SessionDigestBuilder(
        "fr"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        "Tu as travaillé avec"
        in digest.summary
    )


def test_filter_is_prioritized():
    tracker = make_tracker()

    digest = SessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        "filtros"
        in digest.key_learning
    )


def test_digest_has_no_source_code():
    tracker = make_tracker()

    digest = SessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        not hasattr(
            digest,
            "source_code"
        )
    )


def test_invalid_language_fails():
    with pytest.raises(
        ValueError
    ):
        SessionDigestBuilder(
            "xx"
        )
