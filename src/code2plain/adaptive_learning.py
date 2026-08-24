from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptiveExplanation:
    mode: str
    explanation: str
    challenge: str


class AdaptiveLearningEngine:
    def adapt(
        self,
        *,
        concept: str,
        explanation: str,
        challenge: str,
        level: str,
    ) -> AdaptiveExplanation:
        if level == "dominado":
            return AdaptiveExplanation(
                mode="compacto",
                explanation=(
                    f"{concept}: ya lo has trabajado varias veces."
                ),
                challenge=challenge,
            )

        if level == "reforzar":
            return AdaptiveExplanation(
                mode="refuerzo",
                explanation=(
                    explanation
                    + " Presta especial atención a esta parte."
                ),
                challenge=challenge,
            )

        return AdaptiveExplanation(
            mode="normal",
            explanation=explanation,
            challenge=challenge,
        )
