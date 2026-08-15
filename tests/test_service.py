from code2plain.service import Code2PlainService


def test_service_returns_serializable_structure():
    service = Code2PlainService()

    result = service.explain_code(
        """x = 10
print(x)
"""
    )

    assert isinstance(result, dict)
    assert "summary" in result
    assert "sections" in result
    assert len(result["sections"]) == 2


def test_section_has_visual_and_learning_fields():
    service = Code2PlainService()

    result = service.explain_code("total = 100")

    section = result["sections"][0]

    required_fields = {
        "section_number",
        "start_line",
        "end_line",
        "code",
        "title",
        "category",
        "color_tag",
        "what_it_does",
        "what_to_learn",
    }

    assert required_fields.issubset(section.keys())


def test_service_is_ready_for_overlay_contract():
    service = Code2PlainService()

    result = service.explain_code(
        """import pandas as pd
df = pd.read_excel("orders.xlsx")
"""
    )

    first = result["sections"][0]
    second = result["sections"][1]

    assert first["section_number"] == 1
    assert second["section_number"] == 2
    assert first["color_tag"] != second["color_tag"]
