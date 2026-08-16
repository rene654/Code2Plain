from pathlib import Path


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


def test_compact_overlay_exists():
    html = HTML.read_text()

    assert (
        'id="compactLearningOverlay"'
        in html
    )

    assert (
        'id="compactSummaryText"'
        in html
    )

    assert (
        'id="compactLearningText"'
        in html
    )


def test_compact_overlay_is_automatic():
    js = JS.read_text()

    assert (
        "showCompactLearningOverlay("
        in js
    )

    assert (
        "chooseCompactLearningSection"
        in js
    )


def test_compact_overlay_auto_hides():
    js = JS.read_text()

    assert (
        "10000"
        in js
    )

    assert (
        "compactOverlayTimer"
        in js
    )


def test_compact_overlay_is_non_blocking():
    css = CSS.read_text()

    assert (
        "pointer-events: none"
        in css
    )


def test_compact_overlay_is_narrow():
    css = CSS.read_text()

    assert (
        "320px"
        in css
    )


def test_compact_overlay_has_motion():
    css = CSS.read_text()

    assert (
        "@keyframes compactContentIn"
        in css
    )


def test_compact_overlay_supports_reduced_motion():
    css = CSS.read_text()

    assert (
        "prefers-reduced-motion"
        in css
    )
