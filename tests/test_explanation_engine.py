from src.code2plain.engine.explanation_engine import ExplanationEngine


def test_assignment():
    engine = ExplanationEngine()

    result = engine.explain("total = 100")

    assert result.category == "assignment"
    assert "Guarda" in result.summary


def test_print():
    engine = ExplanationEngine()

    result = engine.explain("print(total)")

    assert result.category == "output"


def test_for_loop():
    engine = ExplanationEngine()

    result = engine.explain("for item in items:")

    assert result.category == "loop"


def test_empty_code():
    engine = ExplanationEngine()

    result = engine.explain("")

    assert result.category == "empty"
