from code2plain.learning_motivation import (
    LearningMotivationEngine,
)


engine = LearningMotivationEngine()


def test_new_skill_encourages_understanding():
    feedback = engine.build(
        skill_name="Usar una función",
        seen=1,
        correct=0,
        incorrect=0,
    )

    assert (
        feedback.mastery_level
        == "nuevo"
    )


def test_weak_skill_focuses_practice_without_shame():
    feedback = engine.build(
        skill_name="Seguir información",
        seen=5,
        correct=1,
        incorrect=3,
    )

    assert (
        feedback.mastery_level
        == "reforzar"
    )

    assert "enfocar" in (
        feedback.message
    )


def test_progress_reduces_future_help():
    feedback = engine.build(
        skill_name="Usar una función",
        seen=5,
        correct=3,
        incorrect=1,
    )

    assert (
        feedback.mastery_level
        == "avanzando"
    )

    assert "menos ayuda" in (
        feedback.message
    )


def test_mastered_skill_is_not_overexplained():
    feedback = engine.build(
        skill_name="Usar una función",
        seen=5,
        correct=5,
        incorrect=0,
    )

    assert (
        feedback.mastery_level
        == "dominado"
    )

    assert "dejará de explicarlo" in (
        feedback.next_step
    )
