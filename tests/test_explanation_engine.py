from code2plain.engine.explanation_engine import ExplanationEngine


def test_assignment():
    engine = ExplanationEngine()

    result = engine.explain("total = 100")

    assert result.category == "assignment"
    assert "Guarda" in result.summary


def test_print():
    engine = ExplanationEngine()

    result = engine.explain("print(total)")

    assert result.category == "function_call"
    assert "Muestra" in result.summary


def test_for_loop():
    engine = ExplanationEngine()

    result = engine.explain(
        "for item in items:\n"
        "    print(item)"
    )

    assert result.category == "loop"


def test_empty_code():
    engine = ExplanationEngine()

    result = engine.explain("")

    assert result.category == "empty"


def test_script_is_split_into_sections():
    engine = ExplanationEngine()

    code = """import pandas as pd

df = pd.read_excel("orders.xlsx")

late_orders = df[df["status"] == "Late"]

summary = late_orders.groupby("supplier")["amount"].sum()

summary.to_excel("late_orders.xlsx")
"""

    result = engine.explain_script(code)

    assert len(result.sections) == 5
    assert result.sections[0].section_number == 1
    assert result.sections[0].category == "import"
    assert result.sections[1].category == "assignment"
    assert result.sections[-1].category == "function_call"


def test_sections_have_different_colors():
    engine = ExplanationEngine()

    result = engine.explain_script(
        """import os
x = 10
print(x)
"""
    )

    assert result.sections[0].color_tag == "blue"
    assert result.sections[1].color_tag == "green"
    assert result.sections[2].color_tag == "purple"


def test_section_contains_learning_content():
    engine = ExplanationEngine()

    result = engine.explain_script("total = 100")

    section = result.sections[0]

    assert section.what_it_does
    assert section.what_to_learn
    assert "variables" in section.what_to_learn.lower()


def test_script_summary():
    engine = ExplanationEngine()

    code = """x = 10

if x > 5:
    print(x)
"""

    result = engine.explain_script(code)

    assert len(result.sections) == 2
    assert "2 secciones" in result.summary


def test_function_section():
    engine = ExplanationEngine()

    code = """def calculate_total(price, quantity):
    return price * quantity
"""

    result = engine.explain_script(code)

    assert len(result.sections) == 1
    assert result.sections[0].category == "function"
    assert "calculate_total" in result.sections[0].title


def test_invalid_python_is_handled():
    engine = ExplanationEngine()

    result = engine.explain_script("for x in")

    assert len(result.sections) == 1
    assert result.sections[0].section_number == 1
    assert result.sections[0].what_to_learn
