from code2plain.service import Code2PlainService
from code2plain.live_store import LiveExplanationStore


CODE = """
import pandas as pd

orders = pd.read_excel("orders.xlsx")

late_orders = orders[
    orders["status"] == "Late"
]

totals = (
    late_orders
    .groupby("supplier")["amount"]
    .sum()
)

totals.to_excel("result.xlsx")
""".strip()


EXPECTED_CONCEPTS = [
    "IMPORT",
    "LOAD DATA",
    "FILTER",
    "AGGREGATE",
    "EXPORT",
]


def test_release_pipeline_spanish():
    result = Code2PlainService(
        language="es"
    ).explain_code(CODE)

    assert result["language"] == "es"

    assert [
        section["concept"]
        for section in result["sections"]
    ] == EXPECTED_CONCEPTS

    assert result["quick_summary"]["text"]

    assert (
        "exporta"
        in result["quick_summary"]["text"].lower()
    )


def test_release_pipeline_english():
    result = Code2PlainService(
        language="en"
    ).explain_code(CODE)

    assert result["language"] == "en"

    assert [
        section["concept"]
        for section in result["sections"]
    ] == EXPECTED_CONCEPTS

    assert (
        "exports"
        in result["quick_summary"]["text"].lower()
    )


def test_release_pipeline_french():
    result = Code2PlainService(
        language="fr"
    ).explain_code(CODE)

    assert result["language"] == "fr"

    assert [
        section["concept"]
        for section in result["sections"]
    ] == EXPECTED_CONCEPTS

    assert (
        "exporte"
        in result["quick_summary"]["text"].lower()
    )


def test_release_session_isolation(tmp_path):
    store = LiveExplanationStore(
        tmp_path / "release.db"
    )

    result_a = Code2PlainService(
        language="es"
    ).explain_code(
        "alpha = 1"
    )

    result_b = Code2PlainService(
        language="fr"
    ).explain_code(
        "beta = 2"
    )

    store.publish(
        result_a,
        source="release-gate",
        session_id="alpha",
    )

    store.publish(
        result_b,
        source="release-gate",
        session_id="beta",
    )

    alpha = store.latest(
        session_id="alpha"
    )

    beta = store.latest(
        session_id="beta"
    )

    assert alpha is not None
    assert beta is not None

    assert (
        alpha["explanation"]["code"]
        == "alpha = 1"
    )

    assert (
        beta["explanation"]["code"]
        == "beta = 2"
    )

    assert (
        alpha["explanation"]["language"]
        == "es"
    )

    assert (
        beta["explanation"]["language"]
        == "fr"
    )
