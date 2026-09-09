from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BeginnerExercise:
    kind: str
    concept: str
    prompt: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str


class BeginnerExerciseEngine:
    """
    Builds simple active-learning exercises from
    code the beginner has just seen.
    """

    def build_fill_blank(
        self,
        *,
        code: str,
    ) -> BeginnerExercise | None:
        source = code.strip()

        if "read_csv(" in source:
            return BeginnerExercise(
                kind="fill_blank",
                concept="READ CSV",
                prompt=(
                    'Completa la línea:\n\n'
                    'sales = pd.________("sales.csv")'
                ),
                options=(
                    "read_csv",
                    "groupby",
                    "print",
                ),
                correct_index=0,
                explanation=(
                    "`read_csv` significa leer un archivo CSV. "
                    "Piensa: read = leer."
                ),
            )

        return None


beginner_exercise_engine = BeginnerExerciseEngine()
