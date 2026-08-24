from code2plain.line_learning import (
    LineByLineExplainer,
)


CODE = '''import pandas as pd

sales = pd.read_csv("sales.csv")

active = sales[
    sales["status"] == "active"
]

result = (
    active
    .groupby("customer_id")
    ["amount"]
    .sum()
)

print(result)
'''


def test_line_learning_explains_multiple_lines():
    items = (
        LineByLineExplainer()
        .explain(CODE)
    )

    assert len(items) >= 7

    numbers = {
        item.line_number
        for item in items
    }

    assert 1 in numbers
    assert 3 in numbers


def test_line_learning_keeps_key_concepts():
    items = (
        LineByLineExplainer()
        .explain(CODE)
    )

    concepts = {
        item.concept
        for item in items
        if item.concept
    }

    assert "FILTER" in concepts
    assert "GROUP" in concepts
    assert "AGGREGATE" in concepts


def test_chained_group_select_sum_is_fully_explained():
    code = (
        'result = active.groupby("customer_id")'
        '["amount"].sum()'
    )

    items = (
        LineByLineExplainer()
        .explain(code)
    )

    assert len(items) == 1

    item = items[0]

    assert "GROUP" in item.concept
    assert "SELECT" in item.concept
    assert "AGGREGATE" in item.concept

    assert "Agrupa" in item.explanation
    assert "Selecciona" in item.explanation
    assert "Suma" in item.explanation


def test_every_explained_line_has_learning_metadata():
    code = '''import pandas as pd
sales = pd.read_csv("sales.csv")
print(sales)
'''

    items = (
        LineByLineExplainer()
        .explain(code)
    )

    assert items

    for item in items:
        assert item.explanation
        assert item.why
        assert item.challenge
        assert 1 <= item.confidence <= 100
        assert item.context_status
