from code2plain.adaptive_human_learning import (
    AdaptiveHumanLearningEngine,
)
from code2plain.human_skill_memory import (
    HumanSkillMemoryStore,
)


def test_code_exposure_becomes_skill_progress(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    result = engine.observe_code(
        user_id="rene",
        code=(
            "result = "
            "processor.transform(source)"
        ),
    )

    ids = {
        item.skill_id
        for item in result
    }

    assert "METHOD_CALL" in ids

    progress = memory.get(
        user_id="rene",
        skill_id="METHOD_CALL",
    )

    assert progress.seen == 1


def test_same_skill_accumulates_without_history_rows(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    for _ in range(100):
        engine.observe_code(
            user_id="rene",
            code=(
                "result = "
                "processor.transform(source)"
            ),
        )

    progress = memory.get(
        user_id="rene",
        skill_id="METHOD_CALL",
    )

    rows = memory.list_user_skills(
        user_id="rene"
    )

    assert progress.seen == 100

    assert len(
        [
            row
            for row in rows
            if row.skill_id
            == "METHOD_CALL"
        ]
    ) == 1


def test_persistent_memory_contains_skill_not_source_code(
    tmp_path,
):
    path = tmp_path / "skills.db"

    memory = HumanSkillMemoryStore(
        path
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    secret = (
        "CONFIDENTIAL_CUSTOMER_"
        "ALGORITHM_8821"
    )

    engine.observe_code(
        user_id="privacy-user",
        code=(
            "result = "
            f'processor.transform("{secret}")'
        ),
    )

    raw = path.read_bytes()

    assert (
        secret.encode()
        not in raw
    )

    assert (
        b"METHOD_CALL"
        in raw
    )


def test_users_receive_independent_feedback(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    engine.observe_code(
        user_id="user-a",
        code="result = tool.run(data)",
    )

    engine.observe_code(
        user_id="user-a",
        code="other = tool.run(data)",
    )

    result_b = engine.observe_code(
        user_id="user-b",
        code="result = tool.run(data)",
    )

    method_b = next(
        item
        for item in result_b
        if item.skill_id == "METHOD_CALL"
    )

    assert method_b.seen == 1


def test_correct_answer_updates_mastery(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    feedback = engine.record_answer(
        user_id="rene",
        skill_id="METHOD_CALL",
        correct=True,
    )

    assert feedback.correct == 1
    assert feedback.incorrect == 0
    assert feedback.mastery == 1.0


def test_incorrect_answers_trigger_reinforcement(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    engine.record_answer(
        user_id="rene",
        skill_id="INPUT_OUTPUT",
        correct=False,
    )

    feedback = engine.record_answer(
        user_id="rene",
        skill_id="INPUT_OUTPUT",
        correct=False,
    )

    assert feedback.incorrect == 2

    assert (
        feedback.mastery_level
        == "reforzar"
    )


def test_users_keep_answer_progress_isolated(
    tmp_path,
):
    memory = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    engine = AdaptiveHumanLearningEngine(
        memory=memory
    )

    engine.record_answer(
        user_id="user-a",
        skill_id="FUNCTION_CALL",
        correct=True,
    )

    feedback_b = engine.record_answer(
        user_id="user-b",
        skill_id="FUNCTION_CALL",
        correct=False,
    )

    assert feedback_b.correct == 0
    assert feedback_b.incorrect == 1
