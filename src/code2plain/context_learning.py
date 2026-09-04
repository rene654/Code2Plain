from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextLineExplanation:
    line_number: int
    code: str
    simple_explanation: str
    why_it_matters: str
    input_from: str | None
    output_to: str | None
    consequence: str


class ContextAwareTeachingEngine:
    """
    Explain code using simple language and local context.

    Goal:
    - avoid technical jargon as the primary explanation
    - explain what enters the line
    - explain what the line changes
    - explain where the result goes
    """

    def explain(
        self,
        code: str,
    ) -> list[ContextLineExplanation]:
        lines = code.splitlines()

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return self._fallback(lines)

        assignments = self._collect_assignments(tree)

        results: list[ContextLineExplanation] = []

        for number, raw in enumerate(
            lines,
            start=1,
        ):
            line = raw.strip()

            if not line or line.startswith("#"):
                continue

            explanation = self._explain_line(
                line=line,
                assignments=assignments,
            )

            results.append(
                ContextLineExplanation(
                    line_number=number,
                    code=line,
                    simple_explanation=
                        explanation["simple"],
                    why_it_matters=
                        explanation["why"],
                    input_from=
                        explanation["input"],
                    output_to=
                        explanation["output"],
                    consequence=
                        explanation["consequence"],
                )
            )

        return results

    def _collect_assignments(
        self,
        tree: ast.AST,
    ) -> dict[str, str]:
        assignments: dict[str, str] = {}

        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue

            if len(node.targets) != 1:
                continue

            target = node.targets[0]

            if not isinstance(target, ast.Name):
                continue

            try:
                assignments[target.id] = ast.unparse(
                    node.value
                )
            except Exception:
                assignments[target.id] = ""

        return assignments

    def _explain_line(
        self,
        *,
        line: str,
        assignments: dict[str, str],
    ) -> dict[str, str | None]:
        if line.startswith("import "):
            return {
                "simple":
                    "Carga una herramienta externa "
                    "para poder usarla después.",
                "why":
                    "Sin esta importación, el código "
                    "que depende de esa herramienta "
                    "no funcionaría.",
                "input": None,
                "output": None,
                "consequence":
                    "Si la eliminas, las líneas que "
                    "usan esa librería pueden fallar.",
            }

        if line.startswith("from "):
            return {
                "simple":
                    "Trae una parte específica de "
                    "otra librería o módulo.",
                "why":
                    "Permite usar esa función o clase "
                    "sin escribir el módulo completo.",
                "input": None,
                "output": None,
                "consequence":
                    "Si la eliminas, ese nombre dejará "
                    "de estar disponible.",
            }

        if "read_csv(" in line:
            target = self._assignment_target(line)

            return {
                "simple":
                    "Abre un archivo CSV y guarda "
                    "sus datos para trabajar con ellos.",
                "why":
                    "Primero necesitas cargar los datos "
                    "antes de filtrarlos o analizarlos.",
                "input":
                    "archivo CSV",
                "output":
                    target,
                "consequence":
                    "Si esta línea falla, las operaciones "
                    "que usan esos datos no podrán continuar.",
            }

        if ".groupby(" in line and ".sum()" in line:
            target = self._assignment_target(line)
            source = self._first_name(line)

            return {
                "simple":
                    "Toma los datos anteriores, los separa "
                    "por grupo y suma los valores de cada grupo.",
                "why":
                    "Sirve para convertir muchas filas en "
                    "un resumen útil, por ejemplo un total "
                    "por cliente.",
                "input":
                    source,
                "output":
                    target,
                "consequence":
                    "Si cambias la columna de agrupación, "
                    "cambiará la forma en que se calculan "
                    "los totales.",
            }

        if ".groupby(" in line:
            return {
                "simple":
                    "Junta los datos que comparten "
                    "el mismo valor.",
                "why":
                    "Esto permite calcular resultados "
                    "separados para cada grupo.",
                "input":
                    self._first_name(line),
                "output":
                    self._assignment_target(line),
                "consequence":
                    "Si cambias la columna usada para agrupar, "
                    "los grupos también cambiarán.",
            }

        if ".sum()" in line:
            return {
                "simple":
                    "Suma los valores obtenidos "
                    "en el paso anterior.",
                "why":
                    "Convierte varios números en "
                    "un total.",
                "input":
                    "resultado anterior",
                "output":
                    self._assignment_target(line),
                "consequence":
                    "Si cambias sum() por otra operación, "
                    "el resultado final será distinto.",
            }

        if (
            "[" in line
            and "==" in line
            and "]" in line
        ):
            target = self._assignment_target(line)
            source = self._first_name(line)

            return {
                "simple":
                    "Se queda solo con las filas "
                    "que cumplen esta condición.",
                "why":
                    "Así trabajas únicamente con los datos "
                    "que te interesan.",
                "input":
                    source,
                "output":
                    target,
                "consequence":
                    "Si cambias la condición, cambiarán "
                    "las filas que pasan al siguiente paso.",
            }

        if line.startswith("print("):
            return {
                "simple":
                    "Muestra un resultado en pantalla.",
                "why":
                    "Te permite ver qué produjo el programa.",
                "input":
                    self._inside_call(line),
                "output": None,
                "consequence":
                    "Si la eliminas, el cálculo puede seguir "
                    "funcionando, pero no verás ese resultado.",
            }

        if "=" in line and "==" not in line:
            target = self._assignment_target(line)

            return {
                "simple":
                    f"Guarda el resultado de esta operación "
                    f"en `{target}` para usarlo después.",
                "why":
                    "Guardar el resultado permite que otras "
                    "líneas puedan reutilizarlo.",
                "input":
                    self._first_name(
                        line.split("=", 1)[1]
                    ),
                "output":
                    target,
                "consequence":
                    "Si cambias esta asignación, las líneas "
                    "que usan esa variable pueden recibir "
                    "otro valor.",
            }

        if line in {")", "]", "}"}:
            return {
                "simple":
                    "Cierra una estructura que empezó "
                    "en líneas anteriores.",
                "why":
                    "Python necesita saber dónde termina "
                    "esa expresión.",
                "input": None,
                "output": None,
                "consequence":
                    "Si falta este cierre, el código puede "
                    "tener un error de sintaxis.",
            }

        return {
            "simple":
                "Esta línea continúa la construcción "
                "del bloque actual.",
            "why":
                "Su significado depende de las líneas "
                "que la rodean.",
            "input": None,
            "output": None,
            "consequence":
                "Cambiarla puede modificar el comportamiento "
                "del bloque completo.",
        }

    def _assignment_target(
        self,
        line: str,
    ) -> str | None:
        if "=" not in line or "==" in line:
            return None

        return (
            line.split("=", 1)[0]
            .strip()
            or None
        )

    def _first_name(
        self,
        text: str,
    ) -> str | None:
        try:
            tree = ast.parse(
                text,
                mode="eval",
            )
        except SyntaxError:
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                return node.id

        return None

    def _inside_call(
        self,
        line: str,
    ) -> str | None:
        if "(" not in line or ")" not in line:
            return None

        return (
            line.split("(", 1)[1]
            .rsplit(")", 1)[0]
            .strip()
            or None
        )

    def _fallback(
        self,
        lines: list[str],
    ) -> list[ContextLineExplanation]:
        results = []

        for number, raw in enumerate(
            lines,
            start=1,
        ):
            line = raw.strip()

            if not line:
                continue

            results.append(
                ContextLineExplanation(
                    line_number=number,
                    code=line,
                    simple_explanation=(
                        "Esta línea forma parte "
                        "de un bloque incompleto."
                    ),
                    why_it_matters=(
                        "Necesito más contexto para "
                        "explicarla con precisión."
                    ),
                    input_from=None,
                    output_to=None,
                    consequence=(
                        "Completa el bloque para obtener "
                        "una explicación más confiable."
                    ),
                )
            )

        return results


context_aware_teaching = (
    ContextAwareTeachingEngine()
)
