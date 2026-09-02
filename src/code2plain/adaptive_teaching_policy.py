from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TeachingPolicy:
    level: str
    explanation_depth: str
    show_why: bool
    show_input_output: bool
    show_experiment: bool
    require_check: bool
    message: str | None


class AdaptiveTeachingPolicy:
    """
    Decides how much teaching support a learner receives.

    Exposure alone never reduces teaching support.
    Only demonstrated understanding can reduce help.
    """

    def decide(
        self,
        *,
        seen: int,
        correct: int,
        incorrect: int,
    ) -> TeachingPolicy:
        attempts = (
            correct
            + incorrect
        )

        # ------------------------------------------
        # No evidence of understanding yet
        # ------------------------------------------

        if attempts == 0:
            return TeachingPolicy(
                level="guided",
                explanation_depth="full",
                show_why=True,
                show_input_output=True,
                show_experiment=True,
                require_check=False,
                message=None,
            )

        # ------------------------------------------
        # Learner is struggling
        # ------------------------------------------

        if incorrect > correct:
            return TeachingPolicy(
                level="reinforcement",
                explanation_depth="full",
                show_why=True,
                show_input_output=True,
                show_experiment=True,
                require_check=True,
                message=(
                    "Esta habilidad todavía necesita práctica, "
                    "así que mantendré la explicación completa."
                ),
            )

        # ------------------------------------------
        # First real evidence of understanding
        # ------------------------------------------

        if (
            correct == 1
            and incorrect == 0
        ):
            return TeachingPolicy(
                level="supported",
                explanation_depth="full",
                show_why=True,
                show_input_output=True,
                show_experiment=False,
                require_check=True,
                message=(
                    "Ya mostraste una primera señal "
                    "de comprensión."
                ),
            )

        # ------------------------------------------
        # Consistent progress
        # ------------------------------------------

        if (
            correct >= 2
            and correct > incorrect
            and correct < 5
        ):
            return TeachingPolicy(
                level="reduced",
                explanation_depth="compact",
                show_why=False,
                show_input_output=True,
                show_experiment=False,
                require_check=True,
                message=(
                    "Ya reconoces esta habilidad con "
                    "bastante consistencia, así que "
                    "reduciré parte de la ayuda."
                ),
            )

        # ------------------------------------------
        # Strong demonstrated mastery
        # ------------------------------------------

        if (
            correct >= 5
            and incorrect == 0
        ):
            return TeachingPolicy(
                level="independent",
                explanation_depth="minimal",
                show_why=False,
                show_input_output=False,
                show_experiment=False,
                require_check=False,
                message=(
                    "Esta habilidad ya tiene evidencia "
                    "fuerte de dominio."
                ),
            )

        # ------------------------------------------
        # Mixed evidence
        # ------------------------------------------

        return TeachingPolicy(
            level="supported",
            explanation_depth="full",
            show_why=True,
            show_input_output=True,
            show_experiment=False,
            require_check=True,
            message=(
                "Hay progreso, pero todavía necesito "
                "más evidencia antes de reducir la ayuda."
            ),
        )


adaptive_teaching_policy = (
    AdaptiveTeachingPolicy()
)
