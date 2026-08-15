from dataclasses import dataclass


@dataclass(frozen=True)
class Explanation:
    code: str
    summary: str
    category: str


class ExplanationEngine:
    """Deterministic explanation engine for simple Python statements."""

    def explain(self, code: str) -> Explanation:
        clean_code = code.strip()

        if not clean_code:
            return Explanation(
                code=code,
                summary="No hay código para explicar.",
                category="empty",
            )

        if clean_code.startswith("print("):
            return Explanation(
                code=code,
                summary="Muestra información en pantalla.",
                category="output",
            )

        if clean_code.startswith("for "):
            return Explanation(
                code=code,
                summary="Repite una acción para cada elemento de una colección.",
                category="loop",
            )

        if clean_code.startswith("if "):
            return Explanation(
                code=code,
                summary="Comprueba una condición y ejecuta código solo si se cumple.",
                category="condition",
            )

        if clean_code.startswith("def "):
            return Explanation(
                code=code,
                summary="Crea una función reutilizable que agrupa una tarea específica.",
                category="function",
            )

        if "=" in clean_code and "==" not in clean_code:
            return Explanation(
                code=code,
                summary="Guarda un valor o resultado dentro de una variable.",
                category="assignment",
            )

        return Explanation(
            code=code,
            summary="Esta línea contiene una instrucción de Python que todavía no tiene una regla específica.",
            category="unknown",
        )
