from code2plain.active_modification import (
    active_modification_engine,
)


def test_builds_filter_modification_challenge():
    challenge = active_modification_engine.build(
        code='high_value = sales[sales["amount"] > 1000]'
    )
    assert challenge is not None
    assert challenge.kind == "modify_filter"
    assert challenge.expected_value == 1500
    assert "1500" in challenge.prompt
def test_verifies_correct_filter_modification():
    correct = active_modification_engine.verify(
        original_code=(
            'high_value = sales[sales["amount"] > 1000]'
        ),
        answer=(
            'high_value = sales[sales["amount"] > 1500]'
        ),
    )
    assert correct is True
def test_rejects_incorrect_filter_modification():
    correct = active_modification_engine.verify(
        original_code=(
            'high_value = sales[sales["amount"] > 1000]'
        ),
        answer=(
            'high_value = sales[sales["amount"] > 1200]'
        ),
    )
    assert correct is False
