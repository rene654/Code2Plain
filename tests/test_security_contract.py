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


def test_live_store_does_not_persist_payloads():
    live_store = (
        SOURCE_DIR
        / "live_store.py"
    ).read_text()

    assert "sqlite3" not in live_store
    assert "json.dumps" not in live_store
    assert "INSERT INTO" not in live_store
    assert "write_text" not in live_store
    assert "write_bytes" not in live_store

    assert (
        "_latest_by_session"
        in live_store
    )


