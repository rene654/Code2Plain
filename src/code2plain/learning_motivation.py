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

        if (
            attempts == 0
            and seen <= 1
        ):
            return MotivationalFeedback(
                mastery_level="nuevo",
                message=(
                    f"Estás encontrando por primera vez "
                    f"la habilidad: {skill_name}."
                ),
                next_step=(
                    "Primero observa qué entra, "
                    "qué ocurre y qué resultado sale."
                ),
            )

        if (
            attempts == 0
            and seen > 1
        ):
            return MotivationalFeedback(
                mastery_level="familiarizándose",
                message=(
                    f"Ya has encontrado "
                    f"`{skill_name}` {seen} veces."
                ),
                next_step=(
                    "Verlo varias veces aumenta la "
                    "familiaridad, pero todavía necesitamos "
                    "una respuesta correcta para comprobar "
                    "comprensión."
                ),
            )

        if incorrect > correct:
            return MotivationalFeedback(
                mastery_level="reforzar",
                message=(
                    "Esta habilidad todavía necesita práctica. "
                    "Eso nos muestra exactamente dónde "
                    "conviene enfocar el aprendizaje."
                ),
                next_step=(
                    "La próxima vez recibirás más apoyo "
                    "y una explicación más guiada."
                ),
            )

        if (
            correct == 1
            and incorrect == 0
        ):
            return MotivationalFeedback(
                mastery_level="comprensión inicial",
                message=(
                    f"Reconociste correctamente "
                    f"`{skill_name}` una vez."
                ),
                next_step=(
                    "Es una primera evidencia de comprensión. "
                    "Vamos a comprobarlo de nuevo en otro "
                    "fragmento antes de reducir la ayuda."
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
                    f"`{skill_name}` varias veces "
                    "sin errores."
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
                    f"`{skill_name}` de forma consistente."
                ),
                next_step=(
                    "La próxima vez reduciremos parte "
                    "de la ayuda para comprobar "
                    "que puedes identificarlo solo."
                ),
            )

        return MotivationalFeedback(
            mastery_level="en aprendizaje",
            message=(
                f"Ya estás practicando "
                f"`{skill_name}` con evidencia real."
            ),
            next_step=(
                "Seguiremos comprobando comprensión "
                "con ejemplos de código distintos."
            ),
        )



learning_motivation = (
    LearningMotivationEngine()
)
