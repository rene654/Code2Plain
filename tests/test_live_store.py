from code2plain.live_store import LiveExplanationStore


def test_live_store_starts_empty(tmp_path):
    store = LiveExplanationStore(
        tmp_path / "live.db"
    )

    assert store.latest() is None


def test_live_store_publishes_explanation(tmp_path):
    store = LiveExplanationStore(
        tmp_path / "live.db"
    )

    version = store.publish(
        {
            "summary": "Example",
            "sections": [],
        },
        source="test",
    )

    latest = store.latest()

    assert version == 1
    assert latest is not None

    assert latest["version"] == 1
    assert latest["source"] == "test"

    assert (
        latest["explanation"]["summary"]
        == "Example"
    )


def test_live_store_detects_only_new_versions(tmp_path):
    store = LiveExplanationStore(
        tmp_path / "live.db"
    )

    first = store.publish(
        {
            "summary": "First",
            "sections": [],
        },
        source="test",
    )

    assert (
        store.latest_after(first)
        is None
    )

    second = store.publish(
        {
            "summary": "Second",
            "sections": [],
        },
        source="test",
    )

    latest = store.latest_after(
        first
    )

    assert latest is not None

    assert (
        latest["version"]
        == second
    )

    assert (
        latest["explanation"]["summary"]
        == "Second"
    )


def test_sessions_are_isolated(tmp_path):
    store = LiveExplanationStore(
        tmp_path / "isolated.db"
    )

    store.publish(
        {
            "summary": "Session A",
            "sections": [],
        },
        source="test",
        session_id="session-a",
    )

    store.publish(
        {
            "summary": "Session B",
            "sections": [],
        },
        source="test",
        session_id="session-b",
    )

    session_a = store.latest(
        session_id="session-a"
    )

    session_b = store.latest(
        session_id="session-b"
    )

    assert session_a is not None
    assert session_b is not None

    assert (
        session_a["session_id"]
        == "session-a"
    )

    assert (
        session_b["session_id"]
        == "session-b"
    )

    assert (
        session_a["explanation"]["summary"]
        == "Session A"
    )

    assert (
        session_b["explanation"]["summary"]
        == "Session B"
    )


def test_latest_after_is_session_scoped(
    tmp_path,
):
    store = LiveExplanationStore(
        tmp_path / "scoped.db"
    )

    session_a_version = store.publish(
        {
            "summary": "A1",
            "sections": [],
        },
        source="test",
        session_id="session-a",
    )

    store.publish(
        {
            "summary": "B1",
            "sections": [],
        },
        source="test",
        session_id="session-b",
    )

    assert (
        store.latest_after(
            session_a_version,
            session_id="session-a",
        )
        is None
    )

    second_a = store.publish(
        {
            "summary": "A2",
            "sections": [],
        },
        source="test",
        session_id="session-a",
    )

    latest_a = store.latest_after(
        session_a_version,
        session_id="session-a",
    )

    assert latest_a is not None

    assert (
        latest_a["version"]
        == second_a
    )

    assert (
        latest_a["explanation"]["summary"]
        == "A2"
    )


def test_legacy_database_is_not_loaded_into_ephemeral_store(
    tmp_path,
):
    import sqlite3

    database = (
        tmp_path
        / "legacy.db"
    )

    connection = sqlite3.connect(
        database
    )

    connection.execute(
        """
        CREATE TABLE live_explanations (
            version INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            source TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )

    connection.execute(
        """
        INSERT INTO live_explanations (
            created_at,
            source,
            payload
        )
        VALUES (?, ?, ?)
        """,
        (
            "2026-08-16T00:00:00+00:00",
            "legacy",
            '{"summary": "Legacy", "sections": []}',
        ),
    )

    connection.commit()
    connection.close()

    store = LiveExplanationStore(
        database
    )

    # Privacy boundary:
    # legacy persistent payloads are NOT restored.
    assert store.latest() is None

    # Existing legacy DB is left untouched;
    # the ephemeral store does not write to it.
    assert database.exists()


