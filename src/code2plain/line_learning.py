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
    why: str
    challenge: str
    concept: str | None
    key: bool
    confidence: int
    context_status: str


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

                concepts = [
                    part.concept
                ]

                explanations = [
                    part.explanation
                ]

                if (
                    ".groupby(" in line
                    and (
                        '["' in line
                        or "['" in line
                    )
                ):
                    concepts.append(
                        "SELECT"
                    )

                    explanations.append(
                        "Selecciona la columna que "
                        "se usará dentro de cada grupo."
                    )

                if (
                    ".sum(" in line
                    or line.endswith(".sum()")
                ):
                    if (
                        "AGGREGATE"
                        not in concepts
                    ):
                        concepts.append(
                            "AGGREGATE"
                        )

                        explanations.append(
                            "Suma los valores de cada "
                            "grupo para obtener un total."
                        )

                results.append(
                    LineExplanation(
                        line_number=number,
                        code=line,
                        explanation=(
                            " ".join(
                                explanations
                            )
                        ),
                        why=(
                            self._why(
                                line,
                                concepts
                            )
                        ),
                        challenge=(
                            self._challenge(
                                line,
                                concepts
                            )
                        ),
                        concept=(
                            " + ".join(
                                concepts
                            )
                        ),
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

            plain = self._plain_explanation(
                line
            )

            results.append(
                LineExplanation(
                    line_number=number,
                    code=line,
                    explanation=plain,
                    why=self._plain_why(
                        line
                    ),
                    challenge=self._plain_challenge(
                        line
                    ),
                    concept=None,
                    key=False,
                    confidence=(
                        self._plain_confidence(
                            line
                        )
                    ),
                    context_status=(
                        "contexto suficiente"
                    ),
                )
            )

        return results

    def _why(
        self,
        line: str,
        concepts: list[str],
    ) -> str:
        reasons = []

        if "FILTER" in concepts:
            reasons.append(
                "Porque necesitamos decidir qué datos conservar."
            )

        if "GROUP" in concepts:
            reasons.append(
                "Porque necesitamos organizar los datos en grupos antes de resumirlos."
            )

        if "SELECT" in concepts:
            reasons.append(
                "Porque el cálculo debe aplicarse únicamente a la columna seleccionada."
            )

        if "AGGREGATE" in concepts:
            reasons.append(
                "Porque queremos convertir varios valores en un resultado resumido."
            )

        return " ".join(reasons)


    def _challenge(
        self,
        line: str,
        concepts: list[str],
    ) -> str:
        if "AGGREGATE" in concepts:
            return (
                "¿Qué cambiaría si usas mean() "
                "en lugar de sum()?"
            )

        if "FILTER" in concepts:
            return (
                "¿Qué datos cambiarían si modificas "
                "la condición?"
            )

        if "GROUP" in concepts:
            return (
                "¿Qué cambiaría si agrupas por otra columna?"
            )

        return (
            "¿Qué crees que cambiaría si modificas esta línea?"
        )


    def _plain_why(
        self,
        line: str,
    ) -> str:
        if (
            line.startswith("import ")
            or line.startswith("from ")
        ):
            return (
                "Porque el programa necesita acceder "
                "a funciones que no están definidas aquí."
            )

        if "read_csv(" in line:
            return (
                "Porque necesitamos cargar los datos "
                "antes de analizarlos."
            )

        if line.startswith("print("):
            return (
                "Porque queremos observar el resultado "
                "producido por el programa."
            )

        if line in {")", "]", "}"}:
            return (
                "Porque una expresión abierta anteriormente "
                "debe cerrarse correctamente."
            )

        if "=" in line and "==" not in line:
            return (
                "Porque necesitamos conservar ese resultado "
                "para utilizarlo posteriormente."
            )

        return (
            "Porque esta instrucción forma parte "
            "de la construcción del flujo del programa."
        )


    def _plain_challenge(
        self,
        line: str,
    ) -> str:
        if "read_csv(" in line:
            return (
                "¿Qué archivo intentaría leer si cambias "
                "el nombre dentro de read_csv()?"
            )

        if line.startswith("print("):
            return (
                "¿Qué aparecería si eliminas esta línea?"
            )

        if "=" in line and "==" not in line:
            return (
                "¿Dónde se vuelve a utilizar el valor "
                "guardado en esta variable?"
            )

        return (
            "¿Qué ocurriría si eliminas esta línea?"
        )


    def _plain_confidence(
        self,
        line: str,
    ) -> int:
        if (
            line.startswith("import ")
            or line.startswith("from ")
            or "read_csv(" in line
            or line.startswith("print(")
            or line in {")", "]", "}"}
        ):
            return 96

        if "=" in line and "==" not in line:
            return 90

        if line.startswith("."):
            return 86

        return 78


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
