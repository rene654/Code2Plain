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

    assert "ayuda" in (
        feedback.next_step
    )

    assert (
        "reduciremos"
        in feedback.next_step
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


def test_exposure_alone_never_claims_understanding():
    feedback = engine.build(
        skill_name="Organizar datos por grupos",
        seen=20,
        correct=0,
        incorrect=0,
    )

    assert feedback.mastery_level == "familiarizándose"

    combined = (
        feedback.message
        + " "
        + feedback.next_step
    ).lower()

    assert "dominad" not in combined
    assert "comprend" not in combined
    assert "correctamente" not in combined


def test_first_incorrect_answer_acknowledges_review_need():
    feedback = engine.build(
        skill_name="Organizar datos por grupos",
        seen=4,
        correct=0,
        incorrect=1,
    )

    assert feedback.mastery_level == "reforzar"

    assert (
        "todavía necesita práctica"
        in feedback.message
    )

    assert (
        "más apoyo"
        in feedback.next_step
    )


def test_first_correct_answer_is_evidence_not_mastery():
    feedback = engine.build(
        skill_name="Organizar datos por grupos",
        seen=4,
        correct=1,
        incorrect=0,
    )

    assert feedback.mastery_level == "comprensión inicial"

    assert (
        "correctamente"
        in feedback.message
    )

    assert "dominad" not in (
        feedback.message
        + feedback.next_step
    ).lower()


def test_repeated_correct_answers_can_reach_mastery():
    feedback = engine.build(
        skill_name="Organizar datos por grupos",
        seen=8,
        correct=5,
        incorrect=0,
    )

    assert feedback.mastery_level == "dominado"
