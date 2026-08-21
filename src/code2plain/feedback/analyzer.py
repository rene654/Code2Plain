from code2plain.feedback.models import (
    CheckFailure,
    LearningFeedback,
)


class FailureAnalyzer:
    """
    Convert a normalized CI/check failure into compact
    learning feedback.

    This layer intentionally avoids long explanations.
    """

    def analyze(
        self,
        failure: CheckFailure,
    ) -> LearningFeedback:
        text = " ".join(
            (
                failure.name,
                failure.summary,
                failure.details,
            )
        ).lower()

        concept = self._detect_concept(text)

        return LearningFeedback(
            status="failed",
            headline="Algo salió mal",
            what_failed=self._what_failed(
                failure,
            ),
            likely_cause=self._likely_cause(
                concept,
            ),
            where_to_look=self._where_to_look(
                failure,
            ),
            concept=concept,
        )

    @staticmethod
    def _detect_concept(
        text: str,
    ) -> str:
        if (
            "syntaxerror" in text
            or "syntax error" in text
        ):
            return "SYNTAX"

        if (
            "modulenotfounderror" in text
            or "importerror" in text
            or "no module named" in text
        ):
            return "IMPORT"

        if "typeerror" in text:
            return "TYPE"

        if (
            "assertionerror" in text
            or "pytest" in text
            or "test failed" in text
        ):
            return "TEST"

        return "DEBUGGING"

    @staticmethod
    def _what_failed(
        failure: CheckFailure,
    ) -> str:
        summary = failure.summary.strip()

        if summary:
            return summary

        return (
            f"El check '{failure.name}' "
            "reportó un fallo."
        )

    @staticmethod
    def _likely_cause(
        concept: str,
    ) -> str:
        causes = {
            "SYNTAX": (
                "Python no pudo interpretar "
                "correctamente una instrucción."
            ),
            "IMPORT": (
                "El programa no pudo encontrar "
                "o cargar una dependencia."
            ),
            "TYPE": (
                "Una operación recibió un tipo "
                "de dato que no esperaba."
            ),
            "TEST": (
                "El resultado real no coincide "
                "con lo que esperaba una prueba."
            ),
            "DEBUGGING": (
                "El check falló y necesita revisar "
                "el contexto específico del error."
            ),
        }

        return causes[concept]

    @staticmethod
    def _where_to_look(
        failure: CheckFailure,
    ) -> str:
        if (
            failure.file_path
            and failure.line
        ):
            return (
                f"{failure.file_path}:"
                f"{failure.line}"
            )

        if failure.file_path:
            return failure.file_path

        return "Revisa el detalle del check."
