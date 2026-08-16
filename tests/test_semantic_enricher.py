from code2plain.service import Code2PlainService


def test_excel_load_is_identified():
    result = Code2PlainService().explain_code(
        'df = pd.read_excel("orders.xlsx")'
    )

    section = result["sections"][0]

    assert section["concept"] == "LOAD DATA"
    assert "Excel" in section["what_it_does"]


def test_boolean_filter_is_identified():
    result = Code2PlainService().explain_code(
        'late_orders = df[df["status"] == "Late"]'
    )

    section = result["sections"][0]

    assert section["concept"] == "FILTER"
    assert "status" in section["what_it_does"]
    assert "Late" in section["what_it_does"]


def test_groupby_sum_is_explained_semantically():
    result = Code2PlainService().explain_code(
        'summary = '
        'late_orders.groupby("supplier")'
        '["amount"].sum()'
    )

    section = result["sections"][0]

    assert section["concept"] == "AGGREGATE"

    assert "supplier" in section["what_it_does"]

    assert "amount" in section["what_it_does"]


def test_excel_export_is_identified():
    result = Code2PlainService().explain_code(
        'summary.to_excel("result.xlsx")'
    )

    section = result["sections"][0]

    assert section["concept"] == "EXPORT"

    assert "output" in (
        section["what_to_learn"].lower()
    )
