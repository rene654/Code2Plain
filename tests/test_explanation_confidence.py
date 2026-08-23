from code2plain.detection.confidence import (
    ExplanationConfidenceAssessor,
)


def test_known_concept_has_high_confidence():
    result = (
        ExplanationConfidenceAssessor()
        .assess(
            code=(
                'grouped = data.groupby("customer")'
            ),
            line_number=1,
            concept="GROUP",
        )
    )

    assert result.score >= 90
    assert (
        result.status
        == "contexto suficiente"
    )


def test_incomplete_code_reduces_confidence():
    result = (
        ExplanationConfidenceAssessor()
        .assess(
            code="result = data.groupby(...)",
            line_number=1,
            concept="GROUP",
        )
    )

    assert result.score < 75
    assert (
        result.status
        == "falta más código"
    )


def test_invalid_line_requests_retry():
    result = (
        ExplanationConfidenceAssessor()
        .assess(
            code="for item in items:",
            line_number=99,
            concept="LOOP",
        )
    )

    assert result.status == "reintentar"
