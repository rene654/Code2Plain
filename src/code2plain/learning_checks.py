from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningCheck:
    question: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str


class LearningCheckEngine:
    """
    Builds small evaluable questions from a semantic
    learning block.

    The check is temporary. It is not persisted as
    user source-code memory.
    """

    def build(
        self,
        *,
        code: str,
        input_from: str | None,
        output_to: str | None,
    ) -> LearningCheck:
        source = code.strip()

        # ------------------------------------------
        # Imports
        # ------------------------------------------

        if (
            source.startswith("import ")
            or source.startswith("from ")
        ):
            return LearningCheck(
                question=(
                    "¿Para qué sirve esta línea "
                    "dentro del programa?"
                ),
                options=(
                    "Para borrar una herramienta externa.",
                    "Para hacer disponible código de otro módulo.",
                    "Para imprimir automáticamente un resultado.",
                ),
                correct_index=1,
                explanation=(
                    "Una importación hace disponible código "
                    "definido en otro módulo para poder usarlo."
                ),
            )

        # ------------------------------------------
        # CSV loading
        # ------------------------------------------

        if "read_csv(" in source:
            return LearningCheck(
                question=(
                    "¿Qué cambia principalmente si usas "
                    "otro archivo dentro de read_csv()?"
                ),
                options=(
                    "Se intentan cargar los datos del nuevo archivo.",
                    "La variable deja de existir.",
                    "Python convierte automáticamente el archivo en código.",
                ),
                correct_index=0,
                explanation=(
                    "read_csv() utiliza la ruta indicada para "
                    "decidir qué archivo de datos debe cargar."
                ),
            )

        # ------------------------------------------
        # Filtering
        # ------------------------------------------

        if (
            "[" in source
            and "==" in source
            and output_to
        ):
            return LearningCheck(
                question=(
                    "¿Qué controla qué filas permanecen "
                    "en el resultado?"
                ),
                options=(
                    "El nombre de la variable de salida.",
                    "La condición que se evalúa.",
                    "La cantidad de líneas del programa.",
                ),
                correct_index=1,
                explanation=(
                    "El filtro conserva únicamente las filas "
                    "para las que la condición resulta verdadera."
                ),
            )

        # ------------------------------------------
        # Group + aggregate
        # ------------------------------------------

        if (
            ".groupby(" in source
            and ".sum()" in source
        ):
            return LearningCheck(
                question=(
                    "¿Qué ocurriría si cambias la columna "
                    "utilizada en groupby()?"
                ),
                options=(
                    "Los datos se organizarían usando grupos diferentes.",
                    "La suma dejaría siempre de funcionar.",
                    "Se eliminaría el DataFrame original.",
                ),
                correct_index=0,
                explanation=(
                    "groupby() decide qué valores se utilizan "
                    "para formar cada grupo."
                ),
            )

        # ------------------------------------------
        # Print
        # ------------------------------------------

        if source.startswith("print("):
            return LearningCheck(
                question=(
                    "Si eliminas esta línea, ¿qué ocurre "
                    "con el cálculo anterior?"
                ),
                options=(
                    "El cálculo puede seguir ocurriendo, "
                    "pero no se muestra aquí.",
                    "Todo el programa deja obligatoriamente de calcular.",
                    "Python borra automáticamente el resultado.",
                ),
                correct_index=0,
                explanation=(
                    "print() muestra un valor; normalmente no es "
                    "la operación que produjo ese valor."
                ),
            )

        # ------------------------------------------
        # Generic input/output fallback
        # ------------------------------------------

        if output_to:
            return LearningCheck(
                question=(
                    "¿Qué papel cumple principalmente "
                    "este bloque?"
                ),
                options=(
                    f"Produce o guarda un resultado en `{output_to}`.",
                    "Solo agrega un comentario al programa.",
                    "Borra todas las variables anteriores.",
                ),
                correct_index=0,
                explanation=(
                    f"El bloque produce un resultado que queda "
                    f"asociado con `{output_to}`."
                ),
            )

        if input_from:
            return LearningCheck(
                question=(
                    "¿Qué dato utiliza este bloque como entrada?"
                ),
                options=(
                    str(input_from),
                    "Ningún dato del programa.",
                    "Siempre un archivo CSV.",
                ),
                correct_index=0,
                explanation=(
                    f"Este bloque utiliza `{input_from}` "
                    "como parte de su entrada."
                ),
            )

        return LearningCheck(
            question=(
                "¿Qué conviene identificar primero "
                "para entender este bloque?"
            ),
            options=(
                "Qué recibe y qué efecto produce.",
                "El color con que aparece en pantalla.",
                "Cuántas letras contiene.",
            ),
            correct_index=0,
            explanation=(
                "Cuando no conocemos una operación, empezar por "
                "su entrada y su efecto evita inventar significado."
            ),
        )


learning_check_engine = LearningCheckEngine()
