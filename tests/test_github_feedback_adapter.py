from code2plain.adapters.github_feedback import (
    GitHubFeedbackAdapter,
)
from code2plain.feedback.service import FeedbackService


def test_github_adapter_normalizes_check():
    adapter = GitHubFeedbackAdapter()

    failure = adapter.normalize_dict(
        {
            "name": "pytest",
            "conclusion": "failure",
            "summary": "1 test failed",
            "details": (
                "AssertionError: expected 10 "
                "but received 8"
            ),
            "file_path": "tests/test_total.py",
            "line": 42,
        }
    )

    assert failure.name == "pytest"
    assert failure.conclusion == "failure"
    assert failure.file_path == (
        "tests/test_total.py"
    )
    assert failure.line == 42


def test_feedback_service_returns_compact_learning_feedback():
    feedback = FeedbackService().from_github_check(
        {
            "name": "pytest",
            "conclusion": "failure",
            "summary": "2 tests failed",
            "details": (
                "AssertionError: expected 10 "
                "but received 8"
            ),
            "file_path": "tests/test_total.py",
            "line": 42,
        }
    )

    assert feedback.status == "failed"
    assert feedback.concept == "TEST"
    assert feedback.what_failed == (
        "2 tests failed"
    )
    assert feedback.where_to_look == (
        "tests/test_total.py:42"
    )
