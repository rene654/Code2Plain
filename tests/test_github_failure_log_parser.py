from code2plain.feedback.github_log_parser import (
    GitHubFailureLogParser,
)


LOG = """
FAILED tests/test_ci_feedback_probe.py::test_ci_feedback_probe - assert (2 + 2) == 5
tests/test_ci_feedback_probe.py:2: AssertionError
E       assert (2 + 2) == 5
"""


def test_parser_extracts_failure_context():
    parsed = GitHubFailureLogParser().parse(
        LOG
    )

    assert parsed.file_path == (
        "tests/test_ci_feedback_probe.py"
    )
    assert parsed.line == 2
    assert "test_ci_feedback_probe" in (
        parsed.summary
    )
    assert parsed.details == (
        "assert (2 + 2) == 5"
    )
