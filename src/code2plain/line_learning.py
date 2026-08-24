from dataclasses import dataclass

from code2plain.detection.confidence import (
    ExplanationConfidenceAssessor,
)
from code2plain.detection.relevance import (
    CodeRelevanceEngine,
)


@dataclass(frozen=True)
class LineExplanation:
    line_number: int
    code: str
    explanation: str
    concept: str | None
    key: bool
    confidence: int | None
    context_status: str | None


class LineByLineExplainer:
    """
    Explain meaningful lines in execution order.

    Important learning lines reuse Code2Plain's
    relevance and confidence engines.
    """

    def __init__(self) -> None:
        self.relevance = CodeRelevanceEngine()
        self.confidence = (
            ExplanationConfidenceAssessor()
        )

    def explain(
        self,
        code: str,
    ) -> list[LineExplanation]:
        important = {
            part.line_number: part
            for part in self.relevance.analyze(
                code
            )
        }

        results = []

        for number, raw in enumerate(
            code.splitlines(),
            start=1,
        ):
            line = raw.strip()

            if (
                not line
                or line.startswith("#")
            ):
                continue

            part = important.get(
                number
            )

            if part is not None:
                confidence = (
                    self.confidence.assess(
                        code=code,
                        line_number=number,
                        concept=part.concept,
                    )
                )

                results.append(
                    LineExplanation(
                        line_number=number,
                        code=line,
                        explanation=(
                            part.explanation
                        ),
                        concept=part.concept,
                        key=True,
                        confidence=(
                            confidence.score
                        ),
                        context_status=(
                            confidence.status
                        ),
                    )
                )

                continue

            results.append(
                LineExplanation(
                    line_number=number,
                    code=line,
                    explanation=(
                        self._plain_explanation(
                            line
                        )
                    ),
                    concept=None,
                    key=False,
                    confidence=None,
                    context_status=None,
                )
            )

        return results

    def _plain_explanation(
        self,
        line: str,
    ) -> str:
        if (
            line.startswith("import ")
            or line.startswith("from ")
        ):
            return (
                "Carga código externo para poder "
                "usar sus funciones en el programa."
            )

        if "read_csv(" in line:
            return (
                "Lee un archivo CSV y guarda "
                "sus datos para trabajar con ellos."
            )

        if line.startswith("print("):
            return (
                "Muestra el resultado en pantalla."
            )

        if (
            line.startswith('["')
            or line.startswith("['")
        ):
            return (
                "Selecciona una columna o elemento "
                "del resultado anterior."
            )

        if line in {
            ")",
            "]",
            "}",
        }:
            return (
                "Cierra la expresión que comenzó "
                "en las líneas anteriores."
            )

        if (
            "=" in line
            and "==" not in line
            and "!=" not in line
            and ">=" not in line
            and "<=" not in line
        ):
            variable = (
                line.split("=", 1)[0]
                .strip()
            )

            return (
                f"Guarda el resultado en "
                f"`{variable}`."
            )

        if line.startswith("."):
            return (
                "Continúa la operación iniciada "
                "en la línea anterior."
            )

        return (
            "Ejecuta esta instrucción como parte "
            "del flujo del programa."
        )


line_by_line_explainer = (
    LineByLineExplainer()
)
