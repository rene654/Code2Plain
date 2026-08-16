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


def test_browser_has_session_preference():
    javascript = JS.read_text()

    assert (
        "code2plain.session"
        in javascript
    )

    assert (
        "currentSessionId"
        in javascript
    )

    assert (
        'get("session")'
        in javascript
    )


def test_live_request_sends_session_id():
    javascript = JS.read_text()

    assert (
        "session_id="
        in javascript
    )

    assert (
        "encodeURIComponent("
        "currentSessionId)"
        in javascript
    )
