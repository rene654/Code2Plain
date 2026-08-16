from __future__ import annotations

from typing import Any


_ACTIONS = {
    "es": {
        "IMPORT":
            "importa herramientas",
        "LOAD DATA":
            "carga datos",
        "FILTER":
            "filtra la información",
        "AGGREGATE":
            "agrupa y resume los datos",
        "EXPORT":
            "exporta el resultado",
        "TRANSFORM":
            "transforma la información",
        "DECIDE":
            "toma una decisión",
        "REPEAT":
            "repite una operación",
        "DEFINE":
            "define una función",
        "CALL":
            "ejecuta una función",
        "RETURN":
            "devuelve un resultado",
        "HANDLE ERROR":
            "maneja posibles errores",
        "MODEL":
            "define una estructura",
        "PROCESS":
            "procesa información",
    },

    "en": {
        "IMPORT":
            "imports tools",
        "LOAD DATA":
            "loads data",
        "FILTER":
            "filters the information",
        "AGGREGATE":
            "groups and summarizes the data",
        "EXPORT":
            "exports the result",
        "TRANSFORM":
            "transforms the information",
        "DECIDE":
            "makes a decision",
        "REPEAT":
            "repeats an operation",
        "DEFINE":
            "defines a function",
        "CALL":
            "runs a function",
        "RETURN":
            "returns a result",
        "HANDLE ERROR":
            "handles possible errors",
        "MODEL":
            "defines a structure",
        "PROCESS":
            "processes information",
    },

    "fr": {
        "IMPORT":
            "importe des outils",
        "LOAD DATA":
            "charge les données",
        "FILTER":
            "filtre les informations",
        "AGGREGATE":
            "regroupe et résume les données",
        "EXPORT":
            "exporte le résultat",
        "TRANSFORM":
            "transforme les informations",
        "DECIDE":
            "prend une décision",
        "REPEAT":
            "répète une opération",
        "DEFINE":
            "définit une fonction",
        "CALL":
            "exécute une fonction",
        "RETURN":
            "retourne un résultat",
        "HANDLE ERROR":
            "gère les erreurs possibles",
        "MODEL":
            "définit une structure",
        "PROCESS":
            "traite les informations",
    },
}


_INTROS = {
    "es":
        "Este código ",
    "en":
        "This code ",
    "fr":
        "Ce code ",
}


class QuickSummaryBuilder:
    """
    Build an instant deterministic summary from the
    semantic concepts already detected by Code2Plain.

    No LLM call is required.
    """

    def __init__(
        self,
        language: str = "es",
    ) -> None:
        self.language = (
            language
            if language in _ACTIONS
            else "en"
        )

    def build(
        self,
        sections: list[
            dict[str, Any]
        ],
    ) -> dict[str, Any]:
        concepts: list[str] = []

        for section in sections:
            concept = section.get(
                "concept",
                "PROCESS",
            )

            if (
                concept not in concepts
            ):
                concepts.append(
                    concept
                )

        actions = [
            _ACTIONS[
                self.language
            ].get(
                concept,
                _ACTIONS[
                    self.language
                ]["PROCESS"],
            )
            for concept in concepts
        ]

        if not actions:
            actions = [
                _ACTIONS[
                    self.language
                ]["PROCESS"]
            ]

        sentence = (
            _INTROS[
                self.language
            ]
            + self._join_actions(
                actions
            )
            + "."
        )

        return {
            "text": sentence,
            "step_count":
                len(sections),
            "concepts":
                concepts,
        }

    def _join_actions(
        self,
        actions: list[str],
    ) -> str:
        if len(actions) == 1:
            return actions[0]

        if self.language == "es":
            conjunction = " y "

        elif self.language == "fr":
            conjunction = " et "

        else:
            conjunction = " and "

        if len(actions) == 2:
            return (
                actions[0]
                + conjunction
                + actions[1]
            )

        return (
            ", ".join(
                actions[:-1]
            )
            + conjunction
            + actions[-1]
        )
