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


def test_recovery_uses_browser_local_storage():
    js = JS.read_text()

    assert (
        "localStorage.setItem"
        in js
    )

    assert (
        "localStorage.getItem"
        in js
    )


def test_recovery_does_not_execute_code():
    js = JS.read_text()

    forbidden = [
        "eval(",
        "new Function(",
    ]

    for item in forbidden:
        assert item not in js
