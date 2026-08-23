from code2plain.detection.learning_pipeline import (
    AutomaticLearningPipeline,
)
from code2plain.detection.models import (
    ContentCandidate,
)


def ai_code(code: str) -> ContentCandidate:
    return ContentCandidate(
        source="chatgpt",
        author_role="assistant",
        content_type="code",
        text=code,
    )


def test_new_relevant_ai_code_teaches():
    pipeline = AutomaticLearningPipeline()

    result = pipeline.process(
        ai_code(
            'active = sales['
            'sales["status"] == "active"]\n'
            'summary = active.groupby("customer_id")'
        )
    )

    assert result.should_teach is True

    concepts = [
        point.concept
        for point in result.learning_points
    ]

    assert concepts == [
        "FILTER",
        "GROUP",
    ]


def test_trivial_ai_code_stays_silent():
    pipeline = AutomaticLearningPipeline()

    result = pipeline.process(
        ai_code(
            'name = "Rene"\n'
            'print(name)'
        )
    )

    assert result.should_teach is False
    assert result.reason == (
        "no_relevant_learning_points"
    )


def test_same_code_does_not_teach_twice():
    pipeline = AutomaticLearningPipeline()

    code = (
        "for item in items:\n"
        "    print(item)"
    )

    first = pipeline.process(
        ai_code(code)
    )

    second = pipeline.process(
        ai_code(code)
    )

    assert first.should_teach is True
    assert second.should_teach is False
    assert second.reason == "already_seen"
