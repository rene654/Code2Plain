from code2plain.learning_memory import (
    LearningMemory,
)


def test_new_concept_starts_learning():
    memory = LearningMemory()

    memory.seen("GROUP")

    assert (
        memory.level("GROUP")
        == "en aprendizaje"
    )


def test_weak_concept_is_marked_for_reinforcement():
    memory = LearningMemory()

    memory.answer(
        "FILTER",
        correct=False,
    )

    assert (
        memory.level("FILTER")
        == "reforzar"
    )


def test_concept_can_become_mastered():
    memory = LearningMemory()

    for _ in range(3):
        memory.answer(
            "AGGREGATE",
            correct=True,
        )

    assert (
        memory.level("AGGREGATE")
        == "dominado"
    )
