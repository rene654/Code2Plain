from code2plain.line_breakdown import line_breakdown_engine


def test_breaks_down_dataframe_filter():
    result = line_breakdown_engine.build(
        code='high_value = sales[sales["amount"] > 1000]'
    )
    assert result is not None
    assert result.title == "Filtro de datos"
    assert len(result.parts) == 4
    assert result.parts[1].code == 'sales["amount"]'
    assert result.parts[2].code == "> 1000"
def test_breaks_down_groupby_sum():
    result = line_breakdown_engine.build(
        code=(
            'summary = '
            'high_value.groupby("region")["amount"].sum()'
        )
    )
    assert result is not None
    assert result.title == "Agrupar y sumar"
    assert len(result.parts) == 5
    assert result.parts[2].code == '.groupby("region")'
    assert result.parts[4].code == ".sum()"
def test_unknown_line_has_no_breakdown():
    result = line_breakdown_engine.build(
        code="print(summary)"
    )
    assert result is None
