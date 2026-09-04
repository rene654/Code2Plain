from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def _premium() -> str:
    source = _source()

    return source.split(
        "CODE2PLAIN PREMIUM LEARNING CARDS",
        1,
    )[1]


def test_premium_learning_card_system_exists():
    premium = _premium()

    assert ".item {" in premium
    assert "var(--c2p-border)" in premium
    assert "var(--c2p-cyan)" in premium
    assert "var(--c2p-surface)" in premium


def test_learning_cards_use_consistent_brand_accent():
    premium = _premium()

    assert (
        "border-left:"
        in premium
    )

    assert (
        "var(--c2p-cyan)"
        in premium
    )

    assert (
        "var(--accent)"
        not in premium.split(
            ".item {",
            1,
        )[1].split(
            "}",
            1,
        )[0]
    )


def test_learning_content_is_compact():
    premium = _premium()

    assert "font-size: 14px;" in premium
    assert "font-size: 13px;" in premium
    assert "padding: 13px 15px;" in premium
    assert "padding: 11px 12px;" in premium


def test_learning_check_has_premium_compact_styles():
    premium = _premium()

    assert ".learning-check {" in premium
    assert ".learning-check-body {" in premium
    assert ".learning-check-option {" in premium
    assert ".learning-check-verify {" in premium


def test_only_one_learning_check_stays_open():
    source = _source()

    assert (
        '".learning-check > summary"'
        in source
    )

    assert (
        '".learning-check[open]"'
        in source
    )

    assert (
        'check.removeAttribute('
        in source
    )

    assert (
        '"open"'
        in source
    )
