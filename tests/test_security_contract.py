from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

SOURCE_DIR = (
    ROOT
    / "src"
    / "code2plain"
)


def test_web_does_not_execute_source_code():
    js = (
        SOURCE_DIR
        / "web"
        / "static"
        / "app.js"
    ).read_text()

    forbidden = [
        "eval(",
        "new Function(",
    ]

    for token in forbidden:
        assert token not in js


def test_live_store_only_serializes_payload():
    live_store = (
        SOURCE_DIR
        / "live_store.py"
    ).read_text()

    assert (
        "json.dumps"
        in live_store
    )

    forbidden = [
        "subprocess.",
        "os.system(",
        "exec(",
    ]

    for token in forbidden:
        assert token not in live_store
