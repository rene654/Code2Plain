from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

CSS = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "static"
    / "styles.css"
)


def test_release_hides_redundant_meta_bar():
    css = CSS.read_text()

    assert (
        ".product-meta-bar"
        in css
    )

    assert (
        "display: none !important"
        in css
    )


def test_release_hides_local_session_note():
    css = CSS.read_text()

    assert (
        ".local-session-note"
        in css
    )


def test_release_hides_duplicate_passive_state():
    css = CSS.read_text()

    assert (
        ".passive-connection-state"
        in css
    )
