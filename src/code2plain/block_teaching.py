from __future__ import annotations

import ast
from dataclasses import dataclass

from code2plain.semantic_blocks import (
    SemanticBlock,
    semantic_block_extractor,
)


@dataclass(frozen=True)
class BlockTeaching:
    start_line: int
    end_line: int
    code: str
    explanation: str
    why: str
    input_from: str | None
    output_to: str | None
    experiment: str


class ContextBlockTeachingEngine:
    def explain(
        self,
        code: str,
    ) -> list[BlockTeaching]:
        blocks = (
            semantic_block_extractor.extract(
                code
            )
        )

        return [
            self._teach(block)
            for block in blocks
        ]

    def _teach(
        self,
        block: SemanticBlock,
    ) -> BlockTeaching:
        expression = block.expression

        if block.kind == "import":
            return self._teach_import(
                block
            )

        if (
            block.kind == "AsyncFunctionDef"
            or block.code.lstrip().startswith(
                "async def lifespan"
            )
        ):
            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    "Define qué debe ocurrir mientras la aplicación "
                    "está funcionando: inicia el administrador de "
                    "sesiones MCP al arrancar y lo mantiene activo "
                    "hasta que la aplicación termina."
                ),
                why=(
                    "El servidor MCP necesita iniciar y cerrar sus "
                    "recursos de forma ordenada junto con la aplicación."
                ),
                input_from="aplicación",
                output_to="ciclo de vida MCP",
                experiment=(
                    "¿Qué recurso dejaría de iniciarse correctamente "
                    "si esta función no se conectara a Starlette?"
                ),
            )

        if (
            block.target == "app"
            and "Starlette(" in expression
        ):
            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    "Crea la aplicación web principal de Code2Plain. "
                    "Las solicitudes que comienzan con `/mcp` se envían "
                    "a `mcp_app`; las demás se envían a `api_app`. "
                    "También conecta `lifespan` para iniciar y cerrar "
                    "correctamente los recursos MCP."
                ),
                why=(
                    "Este bloque une las distintas partes del sistema "
                    "y decide qué aplicación debe atender cada URL."
                ),
                input_from=(
                    "mcp_app + api_app + lifespan"
                ),
                output_to="app",
                experiment=(
                    "Si cambias `/mcp` por `/tools`, ¿en qué dirección "
                    "esperarías encontrar ahora el servidor MCP?"
                ),
            )

        if "read_csv(" in expression:
            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    f"Abre un archivo CSV y guarda "
                    f"sus datos en `{block.target}`."
                ),
                why=(
                    "Los datos deben cargarse antes "
                    "de poder analizarlos."
                ),
                input_from="archivo CSV",
                output_to=block.target,
                experiment=(
                    "¿Qué ocurriría si cambias "
                    "el nombre del archivo?"
                ),
            )

        if self._looks_like_filter(
            expression
        ):
            source = self._first_name(
                expression
            )

            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    f"Toma `{source}` y conserva "
                    f"únicamente las filas que cumplen "
                    f"la condición. El resultado queda "
                    f"guardado en `{block.target}`."
                ),
                why=(
                    "Así el resto del programa trabaja "
                    "solo con los datos que interesan."
                ),
                input_from=source,
                output_to=block.target,
                experiment=(
                    "Cambia el valor de la condición "
                    "y piensa qué filas quedarían."
                ),
            )

        if (
            ".groupby(" in expression
            and ".sum()" in expression
        ):
            source = self._first_name(
                expression
            )

            group = self._groupby_value(
                expression
            )

            column = self._selected_column(
                expression
            )

            explanation = (
                f"Toma `{source}`, junta las filas "
                f"que tienen el mismo `{group}`"
            )

            if column:
                explanation += (
                    f", selecciona `{column}`"
                )

            explanation += (
                " y suma esos valores"
            )

            if block.target:
                explanation += (
                    f". Guarda el resultado "
                    f"en `{block.target}`."
                )
            else:
                explanation += "."

            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=explanation,
                why=(
                    "Convierte muchas filas de datos "
                    "en un resumen útil para cada grupo."
                ),
                input_from=source,
                output_to=block.target,
                experiment=(
                    "¿Qué cambiaría si agrupas "
                    "por otra columna?"
                ),
            )

        if expression.startswith("print("):
            value = self._call_argument(
                expression
            )

            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    f"Muestra `{value}` "
                    "en pantalla."
                ),
                why=(
                    "Te permite observar el resultado "
                    "que produjo el programa."
                ),
                input_from=value,
                output_to=None,
                experiment=(
                    "Elimina temporalmente esta línea: "
                    "¿el cálculo sigue ocurriendo?"
                ),
            )

        if block.target:
            source = self._first_name(
                expression
            )

            return BlockTeaching(
                start_line=block.start_line,
                end_line=block.end_line,
                code=block.code,
                explanation=(
                    f"Calcula un valor y lo guarda "
                    f"en `{block.target}` para "
                    "utilizarlo después."
                ),
                why=(
                    "Una variable permite conservar "
                    "un resultado para otras partes "
                    "del programa."
                ),
                input_from=source,
                output_to=block.target,
                experiment=(
                    f"Busca dónde vuelve a usarse "
                    f"`{block.target}`."
                ),
            )

        return BlockTeaching(
            start_line=block.start_line,
            end_line=block.end_line,
            code=block.code,
            explanation=(
                "Ejecuta esta operación como una "
                "unidad dentro del programa."
            ),
            why=(
                "Su efecto depende de los valores "
                "que recibe y del contexto del bloque."
            ),
            input_from=self._first_name(
                expression
            ),
            output_to=None,
            experiment=(
                "Identifica qué valor utiliza "
                "y qué efecto produce."
            ),
        )

    def _teach_import(
        self,
        block: SemanticBlock,
    ) -> BlockTeaching:
        code = block.code

        explanations = {
            "contextlib": (
                "Carga `contextlib`, una herramienta de Python "
                "para controlar qué debe ocurrir al iniciar y "
                "cerrar ciertos procesos."
            ),
            "AsyncIterator": (
                "Trae `AsyncIterator`, un tipo usado para describir "
                "una operación asíncrona que puede mantenerse activa "
                "durante un periodo."
            ),
            "Starlette": (
                "Trae `Starlette`, la clase que se utilizará "
                "para crear la aplicación web principal."
            ),
            "Mount": (
                "Trae `Mount`, que permite colocar una aplicación "
                "dentro de una ruta específica de otra aplicación."
            ),
            "api_app": (
                "Trae la aplicación API de Code2Plain y la llama "
                "`api_app` para conectarla después a la aplicación principal."
            ),
            "mcp_app": (
                "Trae la aplicación MCP de Code2Plain para conectarla "
                "después a la ruta `/mcp`."
            ),
            "mcp": (
                "Trae el servidor MCP que administra las herramientas "
                "que Code2Plain ofrece mediante MCP."
            ),
        }

        explanation = None

        for name, value in explanations.items():
            if name in code:
                explanation = value
                break

        if explanation is None:
            explanation = (
                "Trae código definido en otro módulo para poder "
                "utilizarlo en este archivo."
            )

        return BlockTeaching(
            start_line=block.start_line,
            end_line=block.end_line,
            code=block.code,
            explanation=explanation,
            why=(
                "Separar el código en módulos evita repetir lógica "
                "y permite construir la aplicación usando piezas especializadas."
            ),
            input_from=None,
            output_to=None,
            experiment=(
                "Busca dónde se utiliza después el nombre "
                "que acaba de importarse."
            ),
        )


    def _looks_like_filter(
        self,
        expression: str,
    ) -> bool:
        return (
            "[" in expression
            and "==" in expression
            and "]" in expression
        )

    def _first_name(
        self,
        expression: str,
    ) -> str | None:
        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )
        except SyntaxError:
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                return node.id

        return None

    def _groupby_value(
        self,
        expression: str,
    ) -> str:
        try:
            start = expression.index(
                ".groupby("
            ) + len(".groupby(")

            end = expression.index(
                ")",
                start,
            )

            return (
                expression[start:end]
                .strip("\"'")
            )
        except ValueError:
            return "grupo"

    def _selected_column(
        self,
        expression: str,
    ) -> str | None:
        marker = ")]"

        try:
            group_end = expression.index(
                ".groupby("
            )

            remainder = expression[
                group_end:
            ]

            close = remainder.index(")")

            after = remainder[
                close + 1:
            ]

            if "[" not in after:
                return None

            start = after.index("[") + 1
            end = after.index("]", start)

            return (
                after[start:end]
                .strip("\"'")
            )
        except ValueError:
            return None

    def _call_argument(
        self,
        expression: str,
    ) -> str | None:
        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            if (
                isinstance(
                    tree.body,
                    ast.Call,
                )
                and tree.body.args
            ):
                return ast.unparse(
                    tree.body.args[0]
                )
        except Exception:
            pass

        return None


context_block_teaching = (
    ContextBlockTeachingEngine()
)
