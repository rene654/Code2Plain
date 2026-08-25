from code2plain.semantic_fallback import (
    SemanticFallbackEngine,
)


def test_unknown_call_requests_more_context():
    result = (
        SemanticFallbackEngine()
        .explain(
            "mystery_engine.execute(data)"
        )
    )

    assert result.needs_more_context is True
    assert result.confidence < 70
    assert (
        result.context_status
        == "contexto insuficiente"
    )


def test_function_structure_is_understood():
    result = (
        SemanticFallbackEngine()
        .explain(
            "def calculate_total(values):\n"
            "    return sum(values)"
        )
    )

    assert result.needs_more_context is False
    assert "calculate_total" in result.explanation
    assert result.confidence >= 80


def test_unknown_assignment_does_not_invent_purpose():
    result = (
        SemanticFallbackEngine()
        .explain(
            "prediction = strange_model.run(data)"
        )
    )

    assert "prediction" in result.explanation
    assert result.needs_more_context is True

    text = result.explanation.lower()

    assert "machine learning" not in text
    assert "inteligencia artificial" not in text


def test_invalid_fragment_requests_context():
    result = (
        SemanticFallbackEngine()
        .explain(
            ".something().another()"
        )
    )

    assert result.needs_more_context is True
    assert result.confidence < 70


def test_unknown_method_call_explains_structure_without_guessing():
    result = (
        SemanticFallbackEngine()
        .explain(
            "result = processor.transform(source)"
        )
    )

    assert "processor.transform" in (
        result.explanation
    )

    assert "source" in (
        result.explanation
    )

    assert "result" in (
        result.explanation
    )

    assert result.needs_more_context is True

    assert "internamente" in (
        result.explanation
    )


def test_unknown_call_includes_keyword_arguments():
    result = (
        SemanticFallbackEngine()
        .explain(
            'processor = '
            'StrangeProcessor(mode="fast")'
        )
    )

    assert "mode='fast'" in (
        result.explanation
    )
