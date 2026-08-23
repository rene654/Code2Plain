from code2plain.detection.relevance import (
    CodeRelevanceEngine,
)


def test_relevance_finds_learning_points():
    code = """
import pandas as pd

sales = pd.read_csv("sales.csv")
active = sales[sales["status"] == "active"]
summary = active.groupby("customer_id")
total = summary["amount"].sum()
"""

    parts = CodeRelevanceEngine().analyze(
        code
    )

    concepts = [
        part.concept
        for part in parts
    ]

    assert concepts == [
        "FILTER",
        "GROUP",
        "AGGREGATE",
    ]


def test_trivial_lines_are_not_highlighted():
    code = """
name = "Rene"
count = 10
print(name)
"""

    parts = CodeRelevanceEngine().analyze(
        code
    )

    assert parts == []


def test_control_flow_is_highlighted():
    code = """
for item in items:
    if item > 10:
        print(item)
"""

    parts = CodeRelevanceEngine().analyze(
        code
    )

    assert [
        part.concept
        for part in parts
    ] == [
        "LOOP",
        "CONDITION",
    ]


def test_function_is_highlighted():
    parts = CodeRelevanceEngine().analyze(
        "def calculate_total(values):\n"
        "    return sum(values)"
    )

    assert len(parts) == 1
    assert parts[0].concept == "FUNCTION"
    assert parts[0].line_number == 1
