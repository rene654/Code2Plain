from code2plain.learning_checks import (
    LearningCheckEngine,
)


engine = LearningCheckEngine()


def test_same_check_keeps_same_option_order():
    first = engine.build(
        code='customer = "Acme"',
        input_from=None,
        output_to="customer",
    )

    second = engine.build(
        code='customer = "Acme"',
        input_from=None,
        output_to="customer",
    )

    assert first.options == second.options
    assert (
        first.correct_index
        == second.correct_index
    )


def test_assignment_checks_vary_correct_position():
    examples = (
        ('customer = "Acme"', "customer"),
        ("orders = 12", "orders"),
        (
            "minimum_orders = 10",
            "minimum_orders",
        ),
    )

    positions = {
        engine.build(
            code=code,
            input_from=None,
            output_to=output_to,
        ).correct_index
        for code, output_to in examples
    }

    assert positions == {0, 1, 2}


def test_reordering_preserves_correct_answer():
    check = engine.build(
        code=(
            'sales = '
            'pd.read_csv("sales.csv")'
        ),
        input_from="archivo CSV",
        output_to="sales",
    )

    correct_option = check.options[
        check.correct_index
    ]

    assert "nuevo archivo" in correct_option
