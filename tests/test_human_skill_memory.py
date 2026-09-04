from code2plain.human_skill_memory import (
    HumanSkillMemoryStore,
)


def test_progress_is_isolated_by_user(
    tmp_path,
):
    store = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    store.record_answer(
        user_id="user-a",
        skill_id="FUNCTION_CALL",
        correct=True,
    )

    store.record_answer(
        user_id="user-b",
        skill_id="FUNCTION_CALL",
        correct=False,
    )

    a = store.get(
        user_id="user-a",
        skill_id="FUNCTION_CALL",
    )

    b = store.get(
        user_id="user-b",
        skill_id="FUNCTION_CALL",
    )

    assert a.correct == 1
    assert a.incorrect == 0

    assert b.correct == 0
    assert b.incorrect == 1


def test_repeated_exposure_does_not_create_history_rows(
    tmp_path,
):
    store = HumanSkillMemoryStore(
        tmp_path / "skills.db"
    )

    for _ in range(1000):
        store.record_seen(
            user_id="rene",
            skill_id="METHOD_CALL",
        )

    progress = store.get(
        user_id="rene",
        skill_id="METHOD_CALL",
    )

    rows = store.list_user_skills(
        user_id="rene"
    )

    assert progress.seen == 1000

    # 1000 bloques estudiados siguen siendo
    # una sola fila agregada de habilidad.
    assert len(rows) == 1


def test_human_skill_db_contains_no_source_code(
    tmp_path,
):
    path = tmp_path / "skills.db"

    store = HumanSkillMemoryStore(
        path
    )

    store.record_seen(
        user_id="privacy-user",
        skill_id="METHOD_CALL",
    )

    raw = path.read_bytes()

    assert (
        b"processor.transform(source)"
        not in raw
    )

    assert (
        b"METHOD_CALL"
        in raw
    )
