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


def test_language_selector_exists():
    html = HTML.read_text()

    assert (
        'id="languageSelector"'
        in html
    )

    assert (
        'value="es"'
        in html
    )

    assert (
        'value="en"'
        in html
    )

    assert (
        'value="fr"'
        in html
    )


def test_language_preference_uses_local_storage():
    js = JS.read_text()

    assert (
        "code2plain.language"
        in js
    )

    assert (
        "localStorage.setItem"
        in js
    )

    assert (
        "localStorage.getItem"
        in js
    )


def test_language_is_sent_to_api():
    js = JS.read_text()

    assert (
        "currentLanguage"
        in js
    )

    assert (
        "language:"
        in js
    )
