from pathlib import Path

import pytest

from code2plain.localization import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
)
from code2plain.service import Code2PlainService


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

HTML = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "index.html"
)


FILTER_CODE = (
    'late_orders = '
    'df[df["status"] == "Late"]'
)


def test_default_language_is_spanish():
    assert (
        DEFAULT_LANGUAGE
        == "es"
    )

    result = (
        Code2PlainService()
        .explain_code(
            FILTER_CODE
        )
    )

    assert (
        result["language"]
        == "es"
    )


def test_supported_languages():
    assert (
        SUPPORTED_LANGUAGES
        == (
            "es",
            "en",
            "fr",
        )
    )


def test_spanish_filter_label():
    result = (
        Code2PlainService(
            language="es"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    section = (
        result["sections"][0]
    )

    assert (
        section["concept"]
        == "FILTER"
    )

    assert (
        section["concept_label"]
        == "FILTRAR (FILTER)"
    )


def test_english_uses_same_concept_id():
    result = (
        Code2PlainService(
            language="en"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    section = (
        result["sections"][0]
    )

    assert (
        section["concept"]
        == "FILTER"
    )

    assert (
        section["concept_label"]
        == "FILTER"
    )

    assert (
        "Filtering"
        in section[
            "learning_modes"
        ]["learn"]["secondary"]
    )


def test_french_uses_same_concept_id():
    result = (
        Code2PlainService(
            language="fr"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    section = (
        result["sections"][0]
    )

    assert (
        section["concept"]
        == "FILTER"
    )

    assert (
        section["concept_label"]
        == "FILTRER (FILTER)"
    )

    assert (
        "Filtrer"
        in section[
            "learning_modes"
        ]["learn"]["secondary"]
    )


def test_deep_filter_changes_language():
    es = (
        Code2PlainService(
            language="es"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    en = (
        Code2PlainService(
            language="en"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    fr = (
        Code2PlainService(
            language="fr"
        )
        .explain_code(
            FILTER_CODE
        )
    )

    es_deep = (
        es["sections"][0]
        ["learning_modes"]["deep"]
    )

    en_deep = (
        en["sections"][0]
        ["learning_modes"]["deep"]
    )

    fr_deep = (
        fr["sections"][0]
        ["learning_modes"]["deep"]
    )

    assert (
        "máscara booleana"
        in es_deep[
            "primary"
        ].lower()
    )

    assert (
        "boolean mask"
        in en_deep[
            "primary"
        ].lower()
    )

    assert (
        "masque booléen"
        in fr_deep[
            "primary"
        ].lower()
    )


def test_spanish_ui_labels():
    html = HTML.read_text()

    assert "Aprender" in html
    assert "Entender" in html
    assert "A fondo" in html
    assert "Explicar código" in html
    assert "HOJA DE ESTUDIO" in html


def test_unsupported_language_fails_cleanly():
    with pytest.raises(
        ValueError
    ):
        Code2PlainService(
            language="de"
        )
