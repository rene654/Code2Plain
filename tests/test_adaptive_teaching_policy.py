from code2plain.adaptive_teaching_policy import (
    AdaptiveTeachingPolicy,
)


policy = AdaptiveTeachingPolicy()


def test_repeated_exposure_does_not_reduce_help():
    result = policy.decide(
        seen=50,
        correct=0,
        incorrect=0,
    )

    assert result.level == "guided"
    assert result.explanation_depth == "full"
    assert result.show_why is True


def test_wrong_answers_increase_support():
    result = policy.decide(
        seen=5,
        correct=0,
        incorrect=2,
    )

    assert result.level == "reinforcement"
    assert result.explanation_depth == "full"
    assert result.require_check is True


def test_first_correct_answer_keeps_support():
    result = policy.decide(
        seen=4,
        correct=1,
        incorrect=0,
    )

    assert result.level == "supported"
    assert result.explanation_depth == "full"


def test_consistent_progress_reduces_help():
    result = policy.decide(
        seen=8,
        correct=3,
        incorrect=0,
    )

    assert result.level == "reduced"
    assert result.explanation_depth == "compact"
    assert result.show_why is False


def test_strong_mastery_becomes_minimal():
    result = policy.decide(
        seen=12,
        correct=5,
        incorrect=0,
    )

    assert result.level == "independent"
    assert result.explanation_depth == "minimal"
    assert result.show_input_output is False


def test_mixed_progress_does_not_claim_mastery():
    result = policy.decide(
        seen=8,
        correct=3,
        incorrect=3,
    )

    assert result.level == "supported"
    assert result.explanation_depth == "full"
