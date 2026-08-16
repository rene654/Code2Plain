from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

JS = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "static"
    / "app.js"
)

CSS = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "static"
    / "styles.css"
)


def test_code_blocks_have_reveal_trigger():
    text = JS.read_text()

    assert "is-revealing" in text

    assert "--block-index" in text


def test_motion_system_has_core_animations():
    text = CSS.read_text()

    assert "@keyframes blockReveal" in text

    assert "@keyframes connectorDraw" in text

    assert "@keyframes highlighterSweep" in text

    assert "@keyframes noteEnter" in text


def test_motion_respects_reduced_motion():
    text = CSS.read_text()

    assert (
        "prefers-reduced-motion"
        in text
    )
