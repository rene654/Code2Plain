from code2plain.block_teaching import (
    ContextBlockTeachingEngine,
)


CODE = '''
import pandas as pd

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


def test_multiline_filter_is_one_learning_block():
    items = (
        ContextBlockTeachingEngine()
        .explain(CODE)
    )

    active = next(
        item
        for item in items
        if item.output_to == "active"
    )

    assert active.start_line == 6
    assert active.end_line == 8

    assert "conserva" in (
        active.explanation
    )

    assert active.input_from == "sales"


def test_multiline_group_sum_is_one_learning_block():
    items = (
        ContextBlockTeachingEngine()
        .explain(CODE)
    )

    result = next(
        item
        for item in items
        if item.output_to == "result"
    )

    assert result.start_line == 10
    assert result.end_line == 15

    assert "customer_id" in (
        result.explanation
    )

    assert "amount" in (
        result.explanation
    )

    assert "suma" in (
        result.explanation
    )

    assert result.input_from == "active"


def test_program_has_five_meaningful_learning_units():
    items = (
        ContextBlockTeachingEngine()
        .explain(CODE)
    )

    assert len(items) == 5


def test_starlette_application_is_explained_as_routing():
    code = '''
app = Starlette(
    routes=[
        Mount("/mcp", app=mcp_app),
        Mount("/", app=api_app),
    ],
    lifespan=lifespan,
)
'''

    item = (
        ContextBlockTeachingEngine()
        .explain(code)[0]
    )

    assert "aplicación web principal" in (
        item.explanation
    )

    assert "/mcp" in item.explanation
    assert "mcp_app" in item.explanation
    assert "api_app" in item.explanation


def test_starlette_import_is_specific():
    item = (
        ContextBlockTeachingEngine()
        .explain(
            "from starlette.applications "
            "import Starlette"
        )[0]
    )

    assert "aplicación web principal" in (
        item.explanation
    )
