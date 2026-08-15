from __future__ import annotations

import ast
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Explanation:
    code: str
    summary: str
    category: str


@dataclass(frozen=True)
class CodeSection:
    section_number: int
    start_line: int
    end_line: int
    code: str
    title: str
    category: str
    color_tag: str
    what_it_does: str
    what_to_learn: str


@dataclass(frozen=True)
class ScriptExplanation:
    code: str
    summary: str
    sections: list[CodeSection] = field(default_factory=list)


class ExplanationEngine:
    """
    Core deterministic explanation engine for Code2Plain.

    Design rule:
    This engine must remain independent from:
    - desktop UI
    - ChatGPT/OpenAI
    - Ralph OS
    - browser extensions
    - external AI providers
    """

    SECTION_COLORS = (
        "blue",
        "green",
        "purple",
        "orange",
        "cyan",
        "yellow",
    )

    def explain(self, code: str) -> Explanation:
        clean_code = code.strip()

        if not clean_code:
            return Explanation(
                code=code,
                summary="No hay código para explicar.",
                category="empty",
            )

        try:
            tree = ast.parse(clean_code)
        except SyntaxError:
            return self._fallback_explain(clean_code)

        if len(tree.body) != 1:
            return Explanation(
                code=code,
                summary=(
                    "Este fragmento contiene varias instrucciones. "
                    "Conviene analizarlo por secciones."
                ),
                category="block",
            )

        node = tree.body[0]

        return Explanation(
            code=code,
            summary=self._what_it_does(node),
            category=self._category_for_node(node),
        )

    def explain_script(self, code: str) -> ScriptExplanation:
        clean_code = code.strip()

        if not clean_code:
            return ScriptExplanation(
                code=code,
                summary="No hay código para explicar.",
                sections=[],
            )

        try:
            tree = ast.parse(code)
        except SyntaxError:
            fallback = self._fallback_explain(code)

            return ScriptExplanation(
                code=code,
                summary=(
                    "El código contiene sintaxis incompleta o inválida, "
                    "por lo que no pudo dividirse estructuralmente."
                ),
                sections=[
                    CodeSection(
                        section_number=1,
                        start_line=1,
                        end_line=max(1, len(code.splitlines())),
                        code=code,
                        title="Código sin clasificar",
                        category=fallback.category,
                        color_tag=self.SECTION_COLORS[0],
                        what_it_does=fallback.summary,
                        what_to_learn=(
                            "Python necesita una estructura sintáctica válida "
                            "antes de poder analizar el código con precisión."
                        ),
                    )
                ],
            )

        sections: list[CodeSection] = []

        for index, node in enumerate(tree.body, start=1):
            start_line = getattr(node, "lineno", 1)
            end_line = getattr(node, "end_lineno", start_line)

            sections.append(
                CodeSection(
                    section_number=index,
                    start_line=start_line,
                    end_line=end_line,
                    code=self._extract_lines(
                        code=code,
                        start_line=start_line,
                        end_line=end_line,
                    ),
                    title=self._title_for_node(node, index),
                    category=self._category_for_node(node),
                    color_tag=self._color_for_section(index),
                    what_it_does=self._what_it_does(node),
                    what_to_learn=self._what_to_learn(node),
                )
            )

        return ScriptExplanation(
            code=code,
            summary=self._build_script_summary(sections),
            sections=sections,
        )

    def _extract_lines(
        self,
        code: str,
        start_line: int,
        end_line: int,
    ) -> str:
        lines = code.splitlines()
        return "\n".join(lines[start_line - 1:end_line])

    def _color_for_section(self, section_number: int) -> str:
        index = (section_number - 1) % len(self.SECTION_COLORS)
        return self.SECTION_COLORS[index]

    def _category_for_node(self, node: ast.AST) -> str:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return "import"

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return "function"

        if isinstance(node, ast.ClassDef):
            return "class"

        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            return "loop"

        if isinstance(node, ast.If):
            return "condition"

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            return "assignment"

        if isinstance(node, ast.Return):
            return "return"

        if isinstance(node, ast.Try):
            return "error_handling"

        if isinstance(node, ast.With):
            return "context"

        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                return "function_call"

            return "expression"

        return "unknown"

    def _title_for_node(
        self,
        node: ast.AST,
        index: int,
    ) -> str:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return "Preparación e importaciones"

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return f"Función: {node.name}"

        if isinstance(node, ast.ClassDef):
            return f"Clase: {node.name}"

        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            return "Proceso repetitivo"

        if isinstance(node, ast.If):
            return "Decisión o validación"

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            return "Preparación o transformación de datos"

        if isinstance(node, ast.Try):
            return "Manejo de errores"

        if isinstance(node, ast.Return):
            return "Resultado"

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return "Ejecución de una acción"

        return f"Sección {index}"

    def _what_it_does(self, node: ast.AST) -> str:
        if isinstance(node, ast.Import):
            modules = ", ".join(alias.name for alias in node.names)

            return (
                f"Importa {modules} para disponer de herramientas "
                "que el programa utilizará después."
            )

        if isinstance(node, ast.ImportFrom):
            module = node.module or "otro módulo"
            names = ", ".join(alias.name for alias in node.names)

            return (
                f"Obtiene {names} desde {module} para utilizarlos "
                "más adelante."
            )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return (
                f"Define la función '{node.name}' y agrupa dentro de ella "
                "una tarea reutilizable."
            )

        if isinstance(node, ast.ClassDef):
            return (
                f"Define la clase '{node.name}', agrupando datos "
                "y comportamientos relacionados."
            )

        if isinstance(node, (ast.For, ast.AsyncFor)):
            return (
                "Recorre varios elementos y ejecuta el mismo bloque "
                "para cada uno."
            )

        if isinstance(node, ast.While):
            return (
                "Repite instrucciones mientras una condición "
                "continúe siendo verdadera."
            )

        if isinstance(node, ast.If):
            return (
                "Evalúa una condición y decide qué instrucciones ejecutar "
                "según el resultado."
            )

        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            return self._describe_assignment(node)

        if isinstance(node, ast.AugAssign):
            return (
                "Actualiza un valor existente realizando una operación "
                "sobre él."
            )

        if isinstance(node, ast.Return):
            return (
                "Entrega un resultado desde una función al lugar "
                "desde donde fue llamada."
            )

        if isinstance(node, ast.Try):
            return (
                "Intenta ejecutar una operación y define una respuesta "
                "si ocurre un error."
            )

        if isinstance(node, ast.With):
            return (
                "Administra temporalmente un recurso y ayuda a cerrarlo "
                "o liberarlo correctamente."
            )

        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                return self._describe_call(node.value)

            return "Ejecuta una expresión de Python."

        return (
            "Ejecuta una instrucción de Python que todavía "
            "no tiene una explicación especializada."
        )

    def _what_to_learn(self, node: ast.AST) -> str:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return (
                "Las importaciones permiten reutilizar librerías y código "
                "que ya existe, en lugar de programarlo todo desde cero."
            )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return (
                "Las funciones separan responsabilidades y permiten "
                "reutilizar una misma lógica sin duplicar código."
            )

        if isinstance(node, ast.ClassDef):
            return (
                "Las clases permiten representar conceptos mediante "
                "datos y comportamientos agrupados."
            )

        if isinstance(node, (ast.For, ast.AsyncFor)):
            return (
                "Un bucle 'for' sirve para automatizar una acción "
                "sobre varios elementos."
            )

        if isinstance(node, ast.While):
            return (
                "Un bucle 'while' repite una acción mientras "
                "una condición siga cumpliéndose."
            )

        if isinstance(node, ast.If):
            return (
                "Las condiciones permiten que un programa tome decisiones "
                "en lugar de ejecutar siempre el mismo camino."
            )

        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            return (
                "Las variables conservan datos o resultados intermedios "
                "para usarlos en pasos posteriores."
            )

        if isinstance(node, ast.Return):
            return (
                "El 'return' permite que una función produzca un resultado "
                "que otras partes del programa pueden utilizar."
            )

        if isinstance(node, ast.Try):
            return (
                "El manejo de errores evita que una falla inesperada "
                "termine el programa sin control."
            )

        if isinstance(node, ast.With):
            return (
                "Los context managers ayudan a trabajar con recursos "
                "de manera segura, como archivos o conexiones."
            )

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return (
                "Una llamada a función ejecuta comportamiento que ya fue "
                "definido en otra parte del programa o librería."
            )

        return (
            "Cada instrucción forma parte de una secuencia lógica: "
            "entrada, transformación, decisión o salida."
        )

    def _describe_assignment(
        self,
        node: ast.Assign | ast.AnnAssign,
    ) -> str:
        value = node.value

        if isinstance(value, ast.Call):
            function_name = self._call_name(value)

            if function_name:
                return (
                    f"Ejecuta '{function_name}' y guarda el resultado "
                    "para utilizarlo después."
                )

        if isinstance(value, ast.Subscript):
            return (
                "Selecciona una parte específica de una colección o tabla "
                "y guarda ese resultado."
            )

        if isinstance(value, ast.BinOp):
            return (
                "Realiza un cálculo y guarda el resultado "
                "en una variable."
            )

        if isinstance(value, ast.Constant):
            return (
                "Guarda un valor fijo en una variable "
                "para utilizarlo posteriormente."
            )

        return (
            "Guarda datos o el resultado de una operación "
            "en una variable."
        )

    def _describe_call(self, call: ast.Call) -> str:
        function_name = self._call_name(call)

        if function_name == "print":
            return "Muestra información en pantalla."

        if function_name:
            return (
                f"Ejecuta '{function_name}' para realizar "
                "una acción dentro del programa."
            )

        return "Ejecuta una función para realizar una acción."

    def _call_name(self, call: ast.Call) -> str | None:
        if isinstance(call.func, ast.Name):
            return call.func.id

        if isinstance(call.func, ast.Attribute):
            parts: list[str] = []
            current: ast.AST = call.func

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            return ".".join(reversed(parts))

        return None

    def _build_script_summary(
        self,
        sections: list[CodeSection],
    ) -> str:
        if not sections:
            return "No se encontraron instrucciones para explicar."

        return (
            f"El script fue dividido en {len(sections)} secciones principales. "
            "Cada sección muestra qué hace el código y qué concepto "
            "de programación conviene aprender."
        )

    def _fallback_explain(self, code: str) -> Explanation:
        clean_code = code.strip()

        if clean_code.startswith("print("):
            return Explanation(
                code=code,
                summary="Muestra información en pantalla.",
                category="output",
            )

        if clean_code.startswith("for "):
            return Explanation(
                code=code,
                summary=(
                    "Repite una acción para cada elemento "
                    "de una colección."
                ),
                category="loop",
            )

        if clean_code.startswith("if "):
            return Explanation(
                code=code,
                summary=(
                    "Comprueba una condición y ejecuta código "
                    "solo si se cumple."
                ),
                category="condition",
            )

        if clean_code.startswith("def "):
            return Explanation(
                code=code,
                summary="Crea una función reutilizable.",
                category="function",
            )

        if "=" in clean_code and "==" not in clean_code:
            return Explanation(
                code=code,
                summary=(
                    "Guarda un valor o resultado dentro "
                    "de una variable."
                ),
                category="assignment",
            )

        return Explanation(
            code=code,
            summary=(
                "Esta instrucción todavía no tiene "
                "una regla específica."
            ),
            category="unknown",
        )
