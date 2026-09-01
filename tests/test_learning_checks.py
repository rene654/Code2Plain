from code2plain.learning_checks import (
    LearningCheckEngine,
)


engine = LearningCheckEngine()


def test_import_has_evaluable_answer():
    check = engine.build(
        code="import pandas as pd",
        input_from=None,
        output_to=None,
    )

    assert len(check.options) == 3
    assert check.options[
        check.correct_index
    ] == (
        "Para hacer disponible código "
        "de otro módulo."
    )


def test_read_csv_has_evaluable_answer():
    check = engine.build(
        code='sales = pd.read_csv("sales.csv")',
        input_from="archivo CSV",
        output_to="sales",
    )

    assert check.correct_index == 0
    assert "nuevo archivo" in (
        check.options[0]
    )


def test_filter_has_evaluable_answer():
    check = engine.build(
        code=(
            'active = sales['
            'sales["status"] == "active"]'
        ),
        input_from="sales",
        output_to="active",
    )

    assert (
        check.options[
            check.correct_index
        ]
        == "La condición que se evalúa."
    )


def test_groupby_has_evaluable_answer():
    check = engine.build(
        code=(
            'result = active'
            '.groupby("customer_id")'
            '["amount"].sum()'
        ),
        input_from="active",
        output_to="result",
    )

    assert check.correct_index == 0
    assert "grupos diferentes" in (
        check.options[0]
    )


def test_print_has_evaluable_answer():
    check = engine.build(
        code="print(result)",
        input_from="result",
        output_to=None,
    )

    assert "puede seguir ocurriendo" in (
        check.options[
            check.correct_index
        ]
    )


def test_unknown_block_still_gets_safe_check():
    check = engine.build(
        code="mystery_engine.execute(data)",
        input_from="data",
        output_to=None,
    )

    assert check.question
    assert len(check.options) == 3
    assert check.explanation
