from code2plain.service import Code2PlainService


def test_all_learning_modes_are_available():
    result = Code2PlainService().explain_code(
        'late_orders = df[df["status"] == "Late"]'
    )

    modes = (
        result["sections"][0]
        ["learning_modes"]
    )

    assert set(modes) == {
        "learn",
        "understand",
        "deep",
    }


def test_understand_mode_differs_from_learn():
    result = Code2PlainService().explain_code(
        'late_orders = df[df["status"] == "Late"]'
    )

    modes = (
        result["sections"][0]
        ["learning_modes"]
    )

    assert (
        modes["learn"]["primary"]
        != modes["understand"]["primary"]
    )

    assert (
        modes["understand"]["primary_label"]
        == "PLAIN ENGLISH"
    )


def test_deep_mode_explains_boolean_mask():
    result = Code2PlainService().explain_code(
        'late_orders = df[df["status"] == "Late"]'
    )

    deep = (
        result["sections"][0]
        ["learning_modes"]["deep"]
    )

    assert "Boolean mask" in deep["primary"]

    assert "df[condition]" in (
        deep["secondary"]
    )


def test_aggregation_deep_dive_teaches_groupby():
    result = Code2PlainService().explain_code(
        'summary = '
        'late_orders.groupby("supplier")'
        '["amount"].sum()'
    )

    deep = (
        result["sections"][0]
        ["learning_modes"]["deep"]
    )

    assert "split" in (
        deep["technical"].lower()
    )

    assert "method chaining" in (
        deep["secondary"].lower()
    )


def test_load_data_understand_mode_has_flow_context():
    result = Code2PlainService().explain_code(
        'df = pd.read_excel("orders.xlsx")'
    )

    understand = (
        result["sections"][0]
        ["learning_modes"]["understand"]
    )

    assert "enters the program" in (
        understand["primary"]
    )
