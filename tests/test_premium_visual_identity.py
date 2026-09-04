from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def _identity() -> str:
    source = _source()

    return source.split(
        "CODE2PLAIN PREMIUM VISUAL IDENTITY",
        1,
    )[1]


def test_reference_palette_is_present():
    identity = _identity()

    for color in (
        "#081f46",
        "#163470",
        "#1165e7",
        "#2c4f91",
        "#a3bbe3",
        "#eaf0f9",
        "#1aa8d9",
    ):
        assert color in identity


def test_primary_action_is_full_width_blue_cta():
    identity = _identity()

    learn = identity.split(
        "#learn {",
        1,
    )[1].split(
        "}",
        1,
    )[0]

    assert "width: 100%;" in learn
    assert "#1165e7" in learn
    assert "linear-gradient" in learn


def test_header_has_premium_surface():
    identity = _identity()

    header = identity.split(
        ".app-header {",
        1,
    )[1].split(
        "}",
        1,
    )[0]

    assert "border-radius: 18px;" in header
    assert "backdrop-filter" in header
    assert "rgba(255, 255, 255, 0.82)" in header


def test_learning_cards_use_consistent_blue_brand_language():
    identity = _identity()

    item = identity.split(
        ".item {",
        1,
    )[1].split(
        "}",
        1,
    )[0]

    assert "var(--c2p-blue)" in item
    assert "linear-gradient" in item


def test_learning_empty_has_visual_anchor():
    identity = _identity()

    assert ".learning-empty::before" in identity
    assert 'content: "✦";' in identity
