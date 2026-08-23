from dataclasses import dataclass


@dataclass(frozen=True)
class RelevantCodePart:
    line_number: int
    code: str
    concept: str
    explanation: str


class CodeRelevanceEngine:
    """
    Find only code parts worth teaching.

    The goal is not to explain every line.
    The goal is to highlight the concepts that
    materially change what the program does.
    """

    def analyze(
        self,
        code: str,
    ) -> list[RelevantCodePart]:
        results: list[RelevantCodePart] = []

        for number, raw_line in enumerate(
            code.splitlines(),
            start=1,
        ):
            line = raw_line.strip()

            if not line:
                continue

            match = self._classify(line)

            if match is None:
                continue

            concept, explanation = match

            results.append(
                RelevantCodePart(
                    line_number=number,
                    code=line,
                    concept=concept,
                    explanation=explanation,
                )
            )

        return results

    @staticmethod
    def _classify(
        line: str,
    ) -> tuple[str, str] | None:
        if ".groupby(" in line:
            return (
                "GROUP",
                "Agrupa datos que comparten un valor.",
            )

        if ".agg(" in line or ".sum(" in line:
            return (
                "AGGREGATE",
                "Combina valores para obtener un resultado.",
            )

        if ".query(" in line:
            return (
                "FILTER",
                "Conserva solo los datos que cumplen una condición.",
            )

        if (
            "[" in line
            and "==" in line
            and "]" in line
        ):
            return (
                "FILTER",
                "Selecciona datos usando una condición True/False.",
            )

        if line.startswith("for "):
            return (
                "LOOP",
                "Repite una operación para cada elemento.",
            )

        if line.startswith("if "):
            return (
                "CONDITION",
                "Ejecuta código solo cuando se cumple una condición.",
            )

        if line.startswith("def "):
            return (
                "FUNCTION",
                "Define una función reutilizable.",
            )

        if line.startswith("class "):
            return (
                "CLASS",
                "Define una estructura para crear objetos.",
            )

        if "try:" == line:
            return (
                "ERROR HANDLING",
                "Intenta ejecutar código que podría fallar.",
            )

        if line.startswith("except"):
            return (
                "ERROR HANDLING",
                "Define qué hacer cuando ocurre un error.",
            )

        return None
