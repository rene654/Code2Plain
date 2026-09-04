from code2plain.detection.microlearning import (
    MicroLearningPlanner,
)
from code2plain.detection.relevance import (
    CodeRelevanceEngine,
)


def test_microlearning_limits_automatic_explanations():
    code = """
def process_sales(sales):
    for sale in sales:
        if sale["active"]:
            filtered = sales[sales["status"] == "active"]
            grouped = filtered.groupby("customer")
            total = grouped["amount"].sum()
"""

    parts = tuple(
        CodeRelevanceEngine().analyze(
            code
        )
    )

    plan = MicroLearningPlanner(
        max_items=3
    ).build(parts)

    assert plan.total_detected > 3
    assert len(plan.items) == 3


def test_high_value_concepts_are_prioritized():
    code = """
for item in items:
    if item["active"]:
        grouped = data.groupby("customer")
"""

    parts = tuple(
        CodeRelevanceEngine().analyze(
            code
        )
    )

    plan = MicroLearningPlanner().build(
        parts
    )

    concepts = [
        item.concept
        for item in plan.items
    ]

    assert concepts[0] == "GROUP"


def test_items_keep_line_for_future_highlight():
    code = """
name = "Rene"
for item in items:
    print(item)
"""

    parts = tuple(
        CodeRelevanceEngine().analyze(
            code
        )
    )

    plan = MicroLearningPlanner().build(
        parts
    )

    assert plan.items[0].line_number == 3
    assert plan.items[0].concept == "LOOP"
