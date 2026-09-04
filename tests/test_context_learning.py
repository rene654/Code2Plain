from code2plain.context_learning import (
    ContextAwareTeachingEngine,
)


def test_filter_is_explained_without_jargon():
    code = (
        'active = sales['
        'sales["status"] == "active"]'
    )

    items = (
        ContextAwareTeachingEngine()
        .explain(code)
    )

    assert len(items) == 1

    text = items[0].simple_explanation

    assert "filas" in text
    assert "condición" in text
    assert "FILTER" not in text


def test_group_and_sum_explain_real_purpose():
    code = (
        'result = active'
        '.groupby("customer_id")'
        '["amount"].sum()'
    )

    item = (
        ContextAwareTeachingEngine()
        .explain(code)[0]
    )

    assert "separa" in (
        item.simple_explanation
    )

    assert "suma" in (
        item.simple_explanation
    )

    assert "total por cliente" in (
        item.why_it_matters
    )


def test_csv_explains_input_and_output():
    item = (
        ContextAwareTeachingEngine()
        .explain(
            'sales = pd.read_csv("sales.csv")'
        )[0]
    )

    assert item.input_from == "archivo CSV"
    assert item.output_to == "sales"


def test_import_is_beginner_friendly():
    item = (
        ContextAwareTeachingEngine()
        .explain(
            "import pandas as pd"
        )[0]
    )

    assert "herramienta externa" in (
        item.simple_explanation
    )
