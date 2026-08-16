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


def test_clear_session_control_exists():
    html = HTML.read_text()

    assert (
        'id="clearSessionButton"'
        in html
    )

    assert (
        "Limpiar sesión"
        in html
    )


def test_empty_state_exists():
    html = HTML.read_text()

    assert (
        'id="emptyLearningState"'
        in html
    )

    assert (
        "Esperando el siguiente código"
        in html
    )


def test_corrupt_recovery_is_cleaned():
    js = JS.read_text()

    assert (
        "localStorage.removeItem"
        in js
    )

    assert (
        "LAST_EXPLANATION_STORAGE_KEY"
        in js
    )


def test_clear_session_logic_exists():
    js = JS.read_text()

    assert (
        "clearStoredLearningState"
        in js
    )

    assert (
        "Sesión limpiada"
        in js
    )


def test_empty_state_has_motion_reduction():
    css = CSS.read_text()

    assert (
        "@keyframes emptyOrbit"
        in css
    )

    assert (
        "prefers-reduced-motion"
        in css
    )
