from code2plain.feedback import (
    CheckFailure,
    FailureAnalyzer,
)


def test_pytest_failure_becomes_compact_feedback():
    failure = CheckFailure(
        name="pytest",
        conclusion="failure",
        summary="2 tests failed",
        details=(
            "AssertionError: expected 10 "
            "but received 8"
        ),
        file_path="tests/test_total.py",
        line=42,
    )

    feedback = FailureAnalyzer().analyze(
        failure
    )

    assert feedback.status == "failed"
    assert feedback.headline == "Algo salió mal"
    assert feedback.what_failed == (
        "2 tests failed"
    )
    assert feedback.concept == "TEST"
    assert feedback.where_to_look == (
        "tests/test_total.py:42"
    )


def test_import_failure_is_classified():
    failure = CheckFailure(
        name="python tests",
        conclusion="failure",
        summary=(
            "ModuleNotFoundError: "
            "No module named 'pandas'"
        ),
    )

    feedback = FailureAnalyzer().analyze(
        failure
    )

    assert feedback.concept == "IMPORT"
    assert "dependencia" in (
        feedback.likely_cause
    )


def test_syntax_failure_is_classified():
    failure = CheckFailure(
        name="lint",
        conclusion="failure",
        summary=(
            "SyntaxError: invalid syntax"
        ),
        file_path="app.py",
        line=12,
    )

    feedback = FailureAnalyzer().analyze(
        failure
    )

    assert feedback.concept == "SYNTAX"
    assert feedback.where_to_look == (
        "app.py:12"
    )


def test_unknown_failure_stays_simple():
    failure = CheckFailure(
        name="build",
        conclusion="failure",
        summary="Build exited with code 1",
    )

    feedback = FailureAnalyzer().analyze(
        failure
    )

    assert feedback.concept == "DEBUGGING"
    assert feedback.where_to_look == (
        "Revisa el detalle del check."
    )
