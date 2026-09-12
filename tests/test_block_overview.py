from code2plain.block_overview import block_overview_engine


def test_builds_complete_pandas_flow():
    result = block_overview_engine.build(
        code=(
            'sales = pd.read_csv("sales.csv")\n'
            'high_value = sales[sales["amount"] > 1000]\n'
            'summary = high_value.groupby("region")'
            '["amount"].sum()\n'
            'print(summary)'
        )
    )
    assert result is not None
    assert len(result.steps) == 4
    assert result.steps[0].title == "Cargar datos"
    assert result.steps[1].title == "Filtrar datos"
    assert result.steps[2].title == "Agrupar y sumar"
    assert result.steps[3].title == "Mostrar resultado"
def test_builds_partial_flow():
    result = block_overview_engine.build(
        code=(
            'high_value = sales[sales["amount"] > 1000]\n'
            'print(high_value)'
        )
    )
    assert result is not None
    assert len(result.steps) == 2
def test_unknown_code_has_no_overview():
    result = block_overview_engine.build(
        code="value = 42"
    )
    assert result is None
