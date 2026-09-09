from code2plain.beginner_exercises import (
    BeginnerExerciseEngine,
)

engine = BeginnerExerciseEngine()


def test_read_csv_builds_fill_blank_exercise():
    exercise = engine.build_fill_blank(
        code='sales = pd.read_csv("sales.csv")',
    )

    assert exercise is not None
    assert exercise.kind == "fill_blank"
    assert exercise.concept == "READ CSV"
    assert "________" in exercise.prompt

    assert (
        exercise.options[
            exercise.correct_index
        ]
        == "read_csv"
    )


def test_unknown_code_does_not_force_exercise():
    exercise = engine.build_fill_blank(
        code="mystery.execute(data)",
    )

    assert exercise is None
