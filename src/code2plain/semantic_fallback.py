import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticFallbackResult:
    explanation: str
    why: str
    confidence: int
    context_status: str
    needs_more_context: bool


class SemanticFallbackEngine:
    """
    Conservative fallback for code that the normal
    teaching rules do not understand.

    It explains only what can be inferred safely from
    Python structure. It must not invent business meaning.
    """

    def explain(
        self,
        code: str,
    ) -> SemanticFallbackResult:
        source = code.strip()

        if not source:
            return self._unknown(
                "No hay código suficiente para analizar."
            )

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return self._unknown(
                "Este fragmento depende de otras líneas "
                "o no forma una instrucción completa."
            )

        if len(tree.body) != 1:
            return self._unknown(
                "Este fragmento contiene varias operaciones "
                "y necesito analizarlas como un bloque."
            )

        node = tree.body[0]

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            return SemanticFallbackResult(
                explanation=(
                    f"Define una función llamada "
                    f"`{node.name}` que podrá ejecutarse "
                    f"desde otras partes del programa."
                ),
                why=(
                    "Una función agrupa instrucciones "
                    "para poder reutilizarlas."
                ),
                confidence=90,
                context_status="estructura comprendida",
                needs_more_context=False,
            )

        if isinstance(node, ast.ClassDef):
            return SemanticFallbackResult(
                explanation=(
                    f"Define una clase llamada "
                    f"`{node.name}` que servirá como "
                    f"plantilla para crear objetos."
                ),
                why=(
                    "Una clase reúne datos y comportamiento "
                    "relacionados dentro de una misma estructura."
                ),
                confidence=90,
                context_status="estructura comprendida",
                needs_more_context=False,
            )

        if isinstance(node, ast.Return):
            return SemanticFallbackResult(
                explanation=(
                    "Devuelve un resultado desde la función "
                    "que contiene esta línea."
                ),
                why=(
                    "Esto permite que quien llamó a la función "
                    "reciba el valor calculado."
                ),
                confidence=88,
                context_status="estructura comprendida",
                needs_more_context=False,
            )

        if isinstance(node, ast.Assign):
            targets = [
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            ]

            if targets:
                name = targets[0]

                value = node.value

                if isinstance(value, ast.Call):
                    call_name = self._call_name(
                        value.func
                    )

                    arguments = [
                        ast.unparse(argument)
                        for argument in value.args
                    ]

                    keywords = [
                        (
                            f"{keyword.arg}="
                            f"{ast.unparse(keyword.value)}"
                        )
                        for keyword in value.keywords
                        if keyword.arg is not None
                    ]

                    all_arguments = (
                        arguments
                        + keywords
                    )

                    if call_name:
                        argument_text = (
                            ", ".join(
                                all_arguments
                            )
                            if all_arguments
                            else "sin argumentos"
                        )

                        return SemanticFallbackResult(
                            explanation=(
                                f"Llama `{call_name}` usando "
                                f"{argument_text} y guarda el "
                                f"resultado en `{name}`. "
                                "No tengo suficiente contexto "
                                "para asegurar qué hace esa "
                                "operación internamente."
                            ),
                            why=(
                                "Puedo reconocer cómo se conecta "
                                "la llamada con sus datos, pero no "
                                "debo inventar el propósito de una "
                                "función desconocida."
                            ),
                            confidence=68,
                            context_status=(
                                "estructura comprendida; "
                                "propósito específico desconocido"
                            ),
                            needs_more_context=True,
                        )

                return SemanticFallbackResult(
                    explanation=(
                        "Calcula o recibe un valor y lo guarda "
                        f"en `{name}` para utilizarlo después."
                    ),
                    why=(
                        "Guardar un valor permite que otras "
                        "partes del programa puedan reutilizarlo."
                    ),
                    confidence=72,
                    context_status=(
                        "estructura comprendida; "
                        "propósito específico desconocido"
                    ),
                    needs_more_context=True,
                )

        if isinstance(node, ast.Expr):
            return SemanticFallbackResult(
                explanation=(
                    "Ejecuta una operación, pero este fragmento "
                    "por sí solo no permite saber con seguridad "
                    "qué efecto tiene dentro del programa."
                ),
                why=(
                    "Necesito conocer qué objeto o función se "
                    "está utilizando para explicar su propósito."
                ),
                confidence=55,
                context_status="contexto insuficiente",
                needs_more_context=True,
            )

        return self._unknown(
            "Reconozco la estructura de Python, pero no tengo "
            "contexto suficiente para explicar con seguridad "
            "qué intenta conseguir este fragmento."
        )

    def _call_name(
        self,
        node: ast.AST,
    ) -> str | None:
        try:
            return ast.unparse(
                node
            )
        except Exception:
            return None


    @staticmethod
    def _unknown(
        explanation: str,
    ) -> SemanticFallbackResult:
        return SemanticFallbackResult(
            explanation=explanation,
            why=(
                "Es mejor pedir más contexto que inventar "
                "una explicación incorrecta."
            ),
            confidence=35,
            context_status="contexto insuficiente",
            needs_more_context=True,
        )


semantic_fallback = SemanticFallbackEngine()
