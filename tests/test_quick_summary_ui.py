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


def test_quick_summary_toast_exists():
    html = HTML.read_text()

    assert (
        'id="quickSummaryToast"'
        in html
    )

    assert (
        'id="quickSummaryText"'
        in html
    )


def test_summary_is_automatic():
    js = JS.read_text()

    assert (
        "showQuickSummary("
        in js
    )

    assert (
        "result?.quick_summary"
        in js
    )


def test_summary_auto_hides():
    js = JS.read_text()

    assert (
        "8500"
        in js
    )


def test_waiting_dots_exist():
    css = CSS.read_text()

    assert (
        "@keyframes passiveWaitingDot"
        in css
    )


def test_summary_is_non_blocking():
    css = CSS.read_text()

    assert (
        "pointer-events: none"
        in css
    )
