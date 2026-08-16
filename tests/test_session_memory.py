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


def test_learning_state_storage_keys_exist():
    js = JS.read_text()

    assert (
        "code2plain.mode"
        in js
    )

    assert (
        "code2plain.activeBlock"
        in js
    )

    assert (
        "code2plain.lastCode"
        in js
    )

    assert (
        "code2plain.lastExplanation"
        in js
    )


def test_last_explanation_can_be_restored():
    js = JS.read_text()

    assert (
        "restoreLastExplanation"
        in js
    )

    assert (
        "JSON.parse"
        in js
    )

    assert (
        "activateSection"
        in js
    )


def test_explanations_are_persisted():
    js = JS.read_text()

    assert (
        "persistLearningState"
        in js
    )

    assert (
        "JSON.stringify(result)"
        in js
    )


def test_learning_mode_is_persisted():
    js = JS.read_text()

    assert (
        "MODE_STORAGE_KEY"
        in js
    )

    assert (
        "restoreModeButtons"
        in js
    )


def test_session_recovery_hint_exists():
    html = HTML.read_text()

    assert (
        "Tu sesión se recuerda localmente"
        in html
    )

    assert (
        ".local-session-note"
        in CSS.read_text()
    )
