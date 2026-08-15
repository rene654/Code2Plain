from code2plain.mcp.server import explain_code


def test_mcp_explain_code_contract():
    result = explain_code(
        """import pandas as pd

df = pd.read_excel("orders.xlsx")
"""
    )

    assert isinstance(result, dict)
    assert "summary" in result
    assert "sections" in result

    assert len(result["sections"]) == 2

    first = result["sections"][0]

    assert first["section_number"] == 1
    assert first["color_tag"]
    assert first["what_it_does"]
    assert first["what_to_learn"]
