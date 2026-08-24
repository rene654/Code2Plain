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
