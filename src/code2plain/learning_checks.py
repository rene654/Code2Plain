from __future__ import annotations

import hashlib
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
        """
        Build a check with a stable but varied option order.

        The API rebuilds the same check when an answer is
        verified, so ordinary random shuffling would make
        selected_index unreliable.
        """
        check = self._build_unordered(
            code=code,
            input_from=input_from,
            output_to=output_to,
        )

        # STABLE OPTION ORDER
        option_count = len(check.options)

        if option_count <= 1:
            return check

        fingerprint = "\x1f".join(
            (
                code.strip(),
                input_from or "",
                output_to or "",
                check.question,
            )
        )

        digest = hashlib.sha256(
            fingerprint.encode("utf-8")
        ).digest()

        rotation = (
            int.from_bytes(
                digest[:2],
                "big",
            )
            % option_count
        )

        reordered_options = (
            check.options[rotation:]
            + check.options[:rotation]
        )

        reordered_correct_index = (
            check.correct_index
            - rotation
        ) % option_count

        return LearningCheck(
            question=check.question,
            options=reordered_options,
            correct_index=reordered_correct_index,
            explanation=check.explanation,
        )

    def _build_unordered(
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

        if source.startswith(
            ("import ", "from ")
        ):
            return LearningCheck(
                question=(
                    "Esta línea dice `import pandas as pd`. "
                    "¿Qué está haciendo?"
                ),
                options=(
                    "Está cargando una herramienta para poder usarla después.",
                    "Está creando automáticamente una tabla con datos.",
                    "Está guardando el resultado final del programa.",
                ),
                correct_index=0,
                explanation=(
                    "Importar significa traer una herramienta al programa "
                    "para poder usarla después. Aquí `pd` será el nombre corto "
                    "para usar pandas."
                ),
            )

        # ------------------------------------------
        # CSV loading
        # ------------------------------------------

        if "read_csv(" in source:
            return LearningCheck(
                question=(
                    "Cuando ves `pd.read_csv(...)`, "
                    "¿qué le estás pidiendo a pandas?"
                ),
                options=(
                    "Que abra ese archivo y cargue sus datos.",
                    "Que cree un archivo CSV nuevo y vacío.",
                    "Que muestre el archivo directamente en pantalla.",
                ),
                correct_index=0,
                explanation=(
                    "`read_csv` significa leer un archivo CSV. "
                    "Piensa: read = leer, CSV = tipo de archivo."
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
                    "En este filtro, ¿qué decide "
                    "qué filas se quedan?"
                ),
                options=(
                    "La condición que compara los datos.",
                    "El nombre que le damos al resultado.",
                    "La primera columna de la tabla.",
                ),
                correct_index=0,
                explanation=(
                    "Piensa en un filtro como un colador: "
                    "solo pasan las filas donde la condición es verdadera."
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
                    "¿Qué hace primero `groupby()` "
                    "antes de aplicar `.sum()`?"
                ),
                options=(
                    "Forma grupos y después suma dentro de cada grupo.",
                    "Suma todo primero y después intenta separar los datos.",
                    "Ordena automáticamente todas las filas alfabéticamente.",
                ),
                correct_index=0,
                explanation=(
                    "Recuerda este orden: groupby = formar grupos; "
                    "sum = sumar dentro de esos grupos."
                ),
            )

        # ------------------------------------------
        # Print
        # ------------------------------------------

        if source.startswith("print("):
            return LearningCheck(
                question=(
                    "Si quitas `print(result)`, "
                    "¿qué cambia normalmente?"
                ),
                options=(
                    "El resultado puede seguir existiendo, pero ya no se muestra.",
                    "La variable `result` se borra automáticamente.",
                    "Python deja de ejecutar todas las líneas anteriores.",
                ),
                correct_index=0,
                explanation=(
                    "Piensa en `print()` como una pantalla: "
                    "muestra el resultado, pero normalmente no lo crea."
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
