from code2plain.service import Code2PlainService


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


def test_languages_keep_same_structure():
    results = {
        language:
            Code2PlainService(
                language=language
            ).explain_code(
                CODE
            )

        for language in (
            "es",
            "en",
            "fr",
        )
    }

    concepts = {
        language: [
            section["concept"]
            for section
            in result["sections"]
        ]

        for language, result
        in results.items()
    }

    assert (
        concepts["es"]
        == concepts["en"]
        == concepts["fr"]
    )


def test_language_changes_copy_not_code():
    es = (
        Code2PlainService(
            language="es"
        )
        .explain_code(CODE)
    )

    en = (
        Code2PlainService(
            language="en"
        )
        .explain_code(CODE)
    )

    fr = (
        Code2PlainService(
            language="fr"
        )
        .explain_code(CODE)
    )

    assert (
        es["code"]
        == en["code"]
        == fr["code"]
        == CODE
    )

    assert (
        es["sections"][2]
        ["concept_label"]
        != en["sections"][2]
        ["concept_label"]
    )

    assert (
        fr["sections"][2]
        ["concept_label"]
        != en["sections"][2]
        ["concept_label"]
    )
