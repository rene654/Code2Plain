from code2plain.human_skills import (
    get_human_skill,
)


def test_method_call_has_beginner_language():
    skill = get_human_skill(
        "METHOD_CALL"
    )

    assert skill is not None

    assert (
        skill.name
        == "Pedirle una acción a un objeto"
    )

    assert "METHOD_CALL" not in (
        skill.simple_meaning
    )


def test_filter_skill_avoids_filter_jargon():
    skill = get_human_skill(
        "DATA_FILTERING"
    )

    assert skill is not None

    assert "condición" in (
        skill.simple_meaning
    )
