from code2plain.learning_memory_store import (
    LearningMemoryStore,
)


def test_learning_memory_store_persists_seen(
    tmp_path,
):
    path = tmp_path / "learning.db"

    store = LearningMemoryStore(
        path
    )

    store.record_seen("GROUP")
    store.record_seen("GROUP")

    data = store.get(
        "GROUP"
    )

    assert data["seen"] == 2


def test_learning_memory_store_persists_answers(
    tmp_path,
):
    path = tmp_path / "learning.db"

    store = LearningMemoryStore(
        path
    )

    store.record_answer(
        "FILTER",
        correct=True,
    )

    store.record_answer(
        "FILTER",
        correct=False,
    )

    data = store.get(
        "FILTER"
    )

    assert data["correct"] == 1
    assert data["incorrect"] == 1
