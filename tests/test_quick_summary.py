from code2plain.service import (
    Code2PlainService,
)


CODE = """
import pandas as pd

orders = pd.read_excel(
    "orders.xlsx"
)

late_orders = orders[
    orders["status"] == "Late"
]

totals = (
    late_orders
    .groupby("supplier")["amount"]
    .sum()
)

totals.to_excel(
    "result.xlsx"
)
""".strip()


def test_quick_summary_is_created():
    result = (
        Code2PlainService()
        .explain_code(CODE)
    )

    summary = (
        result["quick_summary"]
    )

    assert summary["text"]

    assert (
        summary["step_count"]
        == len(
            result["sections"]
        )
    )


def test_spanish_quick_summary():
    result = (
        Code2PlainService(
            language="es"
        )
        .explain_code(CODE)
    )

    text = (
        result["quick_summary"]
        ["text"]
        .lower()
    )

    assert "carga datos" in text
    assert "filtra" in text
    assert "agrupa" in text
    assert "exporta" in text


def test_english_quick_summary():
    result = (
        Code2PlainService(
            language="en"
        )
        .explain_code(CODE)
    )

    text = (
        result["quick_summary"]
        ["text"]
        .lower()
    )

    assert "loads data" in text
    assert "filters" in text
    assert "exports" in text


def test_french_quick_summary():
    result = (
        Code2PlainService(
            language="fr"
        )
        .explain_code(CODE)
    )

    text = (
        result["quick_summary"]
        ["text"]
        .lower()
    )

    assert "charge les données" in text
    assert "filtre" in text
    assert "exporte" in text
