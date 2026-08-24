from code2plain.learning_interaction import (
    LearningInteractionBuilder,
)


def test_group_learning_interaction():
    result = (
        LearningInteractionBuilder()
        .build("GROUP")
    )

    assert result.why
    assert result.challenge
    assert "grupo" in result.why.lower()
