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
