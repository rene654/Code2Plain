from dataclasses import dataclass


@dataclass(frozen=True)
class ExplanationConfidence:
    score: int
    status: str


class ExplanationConfidenceAssessor:
    """
    Estimate how much context Code2Plain has for a
    specific micro-explanation.

    This is explanation confidence, not AI-code
    detection confidence.
    """

    BASE_SCORES = {
        "FILTER": 94,
        "GROUP": 95,
        "AGGREGATE": 95,
        "LOOP": 96,
        "CONDITION": 95,
        "FUNCTION": 92,
        "CLASS": 90,
        "ERROR HANDLING": 90,
    }

    def assess(
        self,
        *,
        code: str,
        line_number: int,
        concept: str,
    ) -> ExplanationConfidence:
        lines = code.splitlines()

        if (
            line_number < 1
            or line_number > len(lines)
        ):
            return ExplanationConfidence(
                score=55,
                status="reintentar",
            )

        line = lines[
            line_number - 1
        ].strip()

        if not line:
            return ExplanationConfidence(
                score=65,
                status="falta más código",
            )

        score = self.BASE_SCORES.get(
            concept,
            86,
        )

        if "..." in line:
            score = min(
                score,
                72,
            )

        if (
            concept in {
                "FUNCTION",
                "CLASS",
                "ERROR HANDLING",
            }
            and len(
                [
                    item
                    for item in lines
                    if item.strip()
                ]
            ) <= 1
        ):
            score = min(
                score,
                80,
            )

        if score >= 90:
            status = "contexto suficiente"
        elif score >= 75:
            status = "falta contexto"
        else:
            status = "falta más código"

        return ExplanationConfidence(
            score=score,
            status=status,
        )
