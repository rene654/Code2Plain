from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def _polish() -> str:
    return _source().split(
        "CODE2PLAIN FINAL PREMIUM POLISH 178D",
        1,
    )[1]


def test_final_premium_polish_exists():
    polish = _polish()

    assert ".product-strip {" in polish
    assert ".code-editor-shell {" in polish
    assert "#results {" in polish


def test_hero_has_real_product_depth():
    polish = _polish()

    assert ".product-strip::before" in polish
    assert ".product-strip::after" in polish
    assert "#061a3a" in polish
    assert "#149ce8" in polish


def test_editor_has_professional_toolbar_and_gutter():
    polish = _polish()

    assert ".code-editor-toolbar {" in polish
    assert ".editor-status::before" in polish
    assert ".code-editor-shell textarea {" in polish
    assert "#f4f7fb 34px" in polish


def test_learning_timeline_is_compact_and_branded():
    polish = _polish()

    assert "#results::before" in polish
    assert ".item::before" in polish
    assert "#1598ef" in polish
    assert "font-size: 13px;" in polish


def test_final_polish_has_mobile_contract():
    polish = _polish()

    assert "@media (max-width: 640px)" in polish
    assert "min-height: 210px;" in polish
    assert "padding-left: 29px;" in polish
