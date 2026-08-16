from code2plain.learning import (
    AdaptiveSessionDigestBuilder,
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


def test_fresh_profile_still_prioritizes_filter():
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

    digest = AdaptiveSessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        digest.focus_concept
        == "FILTER"
    )

    assert (
        digest.focus_status
        == "new"
    )


def test_new_advanced_concept_can_beat_familiar_filter():
    profile = LearningProfile(
        learner_id="learner_1"
    )

    training = SessionLearningTracker(
        learner_id="learner_1",
        session_id="training",
        profile=profile,
    )

    for _ in range(5):
        training.observe_explanation(
            explanation(
                "FILTER",
            )
        )

    current = SessionLearningTracker(
        learner_id="learner_1",
        session_id="current",
        profile=profile,
    )

    current.observe_explanation(
        explanation(
            "FILTER",
            "HANDLE ERROR",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
        "es"
    ).build(
        current.session,
        profile,
    )

    assert (
        profile.concepts[
            "FILTER"
        ].status
        == "familiar"
    )

    assert (
        digest.focus_concept
        == "HANDLE ERROR"
    )


def test_practicing_concept_is_reinforced():
    profile = LearningProfile(
        learner_id="learner_1"
    )

    first = SessionLearningTracker(
        learner_id="learner_1",
        session_id="s1",
        profile=profile,
    )

    first.observe_explanation(
        explanation(
            "AGGREGATE",
        )
    )

    second = SessionLearningTracker(
        learner_id="learner_1",
        session_id="s2",
        profile=profile,
    )

    second.observe_explanation(
        explanation(
            "AGGREGATE",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
        "es"
    ).build(
        second.session,
        profile,
    )

    assert (
        digest.focus_status
        == "practicing"
    )

    assert (
        "Refuerza"
        in digest.key_learning
    )

    assert (
        digest.reinforcement
        is not None
    )


def test_new_concept_is_selected_by_learning_value():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "IMPORT",
            "HANDLE ERROR",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        digest.new_concept
        == "HANDLE ERROR"
    )


def test_familiar_focus_does_not_force_review():
    profile = LearningProfile(
        learner_id="learner_1"
    )

    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
        profile=profile,
    )

    for _ in range(5):
        tracker.observe_explanation(
            explanation(
                "FILTER",
            )
        )

    digest = AdaptiveSessionDigestBuilder(
        "es"
    ).build(
        tracker.session,
        profile,
    )

    assert (
        digest.focus_status
        == "familiar"
    )

    assert digest.review is None


def test_adaptive_digest_supports_english():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
        "en"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        digest.language
        == "en"
    )

    assert (
        "new"
        in digest.key_learning.lower()
    )


def test_adaptive_digest_supports_french():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
        "fr"
    ).build(
        tracker.session,
        tracker.profile,
    )

    assert (
        digest.language
        == "fr"
    )

    assert (
        digest.focus_concept
        == "FILTER"
    )


def test_adaptive_digest_contains_no_source_code():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        explanation(
            "FILTER",
        )
    )

    digest = AdaptiveSessionDigestBuilder(
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
