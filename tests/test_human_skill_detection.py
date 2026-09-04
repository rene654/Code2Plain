from code2plain.human_skill_detection import (
    HumanSkillDetector,
)


detector = HumanSkillDetector()


def test_method_call_maps_to_human_skill():
    skills = detector.detect(
        "result = processor.transform(source)"
    )

    assert "METHOD_CALL" in skills
    assert "VARIABLE_USE" in skills
    assert "INPUT_OUTPUT" in skills


def test_filter_maps_to_human_skill():
    skills = detector.detect(
        'active = sales['
        'sales["status"] == "active"]'
    )

    assert "DATA_FILTERING" in skills


def test_group_sum_maps_to_human_skills():
    skills = detector.detect(
        'result = active'
        '.groupby("customer_id")'
        '["amount"].sum()'
    )

    assert "DATA_GROUPING" in skills
    assert "DATA_SUMMARY" in skills


def test_import_maps_to_external_tool_skill():
    skills = detector.detect(
        "import pandas as pd"
    )

    assert skills == [
        "IMPORT_USE"
    ]


def test_invalid_code_does_not_invent_skills():
    skills = detector.detect(
        ".unknown().thing()"
    )

    assert skills == []


def test_primary_skill_prefers_method_over_variable():
    from code2plain.human_skill_detection import (
        primary_human_skill,
    )

    result = primary_human_skill(
        "result = processor.transform(source)"
    )

    assert result == "METHOD_CALL"


def test_primary_skill_prefers_filter_for_filtering():
    from code2plain.human_skill_detection import (
        primary_human_skill,
    )

    result = primary_human_skill(
        'active = sales['
        'sales["status"] == "active"]'
    )

    assert result == "DATA_FILTERING"
