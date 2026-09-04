from code2plain.detection.models import (
    ContentCandidate,
)
from code2plain.detection.pipeline import (
    DetectionPipeline,
)


def candidate(code: str) -> ContentCandidate:
    return ContentCandidate(
        source="chatgpt",
        author_role="assistant",
        content_type="code",
        text=code,
    )


def test_new_ai_code_is_explained():
    pipeline = DetectionPipeline()

    result = pipeline.process(
        candidate(
            "total = sum(values)\nprint(total)"
        )
    )

    assert result.should_explain is True


def test_same_ai_code_is_not_explained_twice():
    pipeline = DetectionPipeline()

    code = "total = sum(values)\nprint(total)"

    first = pipeline.process(
        candidate(code)
    )

    second = pipeline.process(
        candidate(code)
    )

    assert first.should_explain is True
    assert second.should_explain is False
    assert second.reason == "already_seen"


def test_changed_code_is_treated_as_new():
    pipeline = DetectionPipeline()

    first = pipeline.process(
        candidate(
            "total = sum(values)\nprint(total)"
        )
    )

    second = pipeline.process(
        candidate(
            "total = sum(values)\nprint(total + tax)"
        )
    )

    assert first.should_explain is True
    assert second.should_explain is True
