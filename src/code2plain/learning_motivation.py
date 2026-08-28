from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MotivationalFeedback:
    mastery_level: str
    message: str
    next_step: str


class LearningMotivationEngine:
    """
    Encouragement based on observable learning progress.

    No empty praise.
    No shame.
    No artificial urgency.
    """

    def build(
        self,
        *,
        skill_name: str,
        seen: int,
        correct: int,
        incorrect: int,
    ) -> MotivationalFeedback:
        attempts = (
            correct
            + incorrect
        )

        if seen <= 1:
            return MotivationalFeedback(
                mastery_level="nuevo",
                message=(
                    f"Estás encontrando por primera vez "
                    f"la habilidad: {skill_name}."
                ),
                next_step=(
                    "Primero entiende qué entra "
                    "y qué resultado produce."
                ),
            )

        if (
            attempts >= 2
            and incorrect > correct
        ):
            return MotivationalFeedback(
                mastery_level="reforzar",
                message=(
                    f"Esta habilidad todavía necesita práctica. "
                    f"Eso nos indica exactamente dónde enfocar "
                    f"las siguientes explicaciones."
                ),
                next_step=(
                    "La próxima vez recibirás una explicación "
                    "más guiada y una pregunta sencilla."
                ),
            )

        if (
            correct >= 4
            and incorrect == 0
        ):
            return MotivationalFeedback(
                mastery_level="dominado",
                message=(
                    f"Has reconocido correctamente "
                    f"`{skill_name}` varias veces."
                ),
                next_step=(
                    "Code2Plain dejará de explicarlo "
                    "desde cero salvo que vuelvas "
                    "a necesitar ayuda."
                ),
            )

        if (
            correct >= 2
            and correct > incorrect
        ):
            return MotivationalFeedback(
                mastery_level="avanzando",
                message=(
                    f"Ya estás reconociendo "
                    f"`{skill_name}` con menos ayuda."
                ),
                next_step=(
                    "La próxima vez reduciremos parte "
                    "de la explicación para comprobar "
                    "que puedes identificarlo solo."
                ),
            )

        return MotivationalFeedback(
            mastery_level="en aprendizaje",
            message=(
                f"Ya has visto `{skill_name}` "
                f"{seen} veces. La familiaridad "
                f"está aumentando."
            ),
            next_step=(
                "Seguiremos practicándolo dentro "
                "de código real."
            ),
        )


learning_motivation = (
    LearningMotivationEngine()
)
