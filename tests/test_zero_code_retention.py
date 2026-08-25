from pathlib import Path

from code2plain.live_store import (
    LiveExplanationStore,
)
from code2plain.learning_memory_store import (
    LearningMemoryStore,
)


SECRET = (
    "TOP_SECRET_CLIENT_"
    "ALGORITHM_X9281"
)


def test_live_payload_is_memory_only(
    tmp_path,
):
    requested_db = (
        tmp_path / "live.db"
    )

    store = LiveExplanationStore(
        requested_db
    )

    store.publish(
        {
            "code": SECRET,
            "explanation":
                "Temporary explanation",
        },
        source="test",
        session_id="privacy",
    )

    result = store.latest(
        session_id="privacy"
    )

    assert result is not None

    # Data may exist transiently in RAM.
    assert (
        result["explanation"]["code"]
        == SECRET
    )

    # But no persistent live database is created.
    assert not requested_db.exists()


def test_learning_memory_stores_concepts_not_code(
    tmp_path,
):
    path = (
        tmp_path
        / "learning.db"
    )

    store = LearningMemoryStore(
        path
    )

    store.record_seen(
        "FUNCTION_CALL"
    )

    raw = path.read_bytes()

    assert (
        SECRET.encode()
        not in raw
    )

    assert (
        b"FUNCTION_CALL"
        in raw
    )


def test_secret_not_found_in_persistent_privacy_files(
    tmp_path,
):
    learning_path = (
        tmp_path
        / "learning.db"
    )

    memory = LearningMemoryStore(
        learning_path
    )

    memory.record_seen(
        "UNKNOWN_FUNCTION_CALL"
    )

    for path in tmp_path.rglob("*"):
        if not path.is_file():
            continue

        assert (
            SECRET.encode()
            not in path.read_bytes()
        )


def test_live_store_has_no_persistent_database_path():
    store = LiveExplanationStore()

    assert store.path is None


def test_live_store_does_not_create_default_live_database(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(
        tmp_path
    )

    store = LiveExplanationStore()

    store.publish(
        {
            "code":
                "CONFIDENTIAL_CUSTOMER_CODE_7391"
        },
        source="privacy-test",
    )

    assert not (
        tmp_path
        / ".code2plain"
        / "live_state.db"
    ).exists()
