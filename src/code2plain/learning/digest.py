from __future__ import annotations

from dataclasses import dataclass

from code2plain.learning.models import (
    LearningProfile,
    LearningSession,
)


_LABELS = {
    "es": {
        "IMPORT": "importaciones",
        "LOAD DATA": "carga de datos",
        "FILTER": "filtros",
        "AGGREGATE": "agrupaciones",
        "EXPORT": "exportación",
        "TRANSFORM": "transformaciones",
        "VALIDATE": "validaciones",
        "REPEAT": "bucles",
        "DECIDE": "condiciones",
        "CALL": "llamadas a funciones",
        "RETURN": "retornos",
        "DEFINE": "definiciones",
        "HANDLE ERROR": "manejo de errores",
        "MODEL": "modelos y clases",
    },
    "en": {
        "IMPORT": "imports",
        "LOAD DATA": "data loading",
        "FILTER": "filters",
        "AGGREGATE": "aggregation",
        "EXPORT": "exports",
        "TRANSFORM": "transformations",
        "VALIDATE": "validation",
        "REPEAT": "loops",
        "DECIDE": "conditions",
        "CALL": "function calls",
        "RETURN": "returns",
        "DEFINE": "definitions",
        "HANDLE ERROR": "error handling",
        "MODEL": "models and classes",
    },
    "fr": {
        "IMPORT": "imports",
        "LOAD DATA": "chargement de données",
        "FILTER": "filtres",
        "AGGREGATE": "agrégations",
        "EXPORT": "exportation",
        "TRANSFORM": "transformations",
        "VALIDATE": "validations",
        "REPEAT": "boucles",
        "DECIDE": "conditions",
        "CALL": "appels de fonctions",
        "RETURN": "retours",
        "DEFINE": "définitions",
        "HANDLE ERROR": "gestion des erreurs",
        "MODEL": "modèles et classes",
    },
}


@dataclass(frozen=True)
class SessionDigest:
    language: str
    summary: str
    key_learning: str
    new_concept: str | None
    review: str | None
    concept_count: int
    explanation_count: int


class SessionDigestBuilder:
    def __init__(
        self,
        language: str = "es",
    ) -> None:

        if language not in _LABELS:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        self.language = language


    def build(
        self,
        session: LearningSession,
        profile: LearningProfile,
    ) -> SessionDigest:

        concepts = list(
            session.concept_counts
        )

        labels = [
            self._label(
                concept
            )
            for concept in concepts
        ]

        key_concept = (
            self._choose_key_concept(
                session
            )
        )

        new_concept = (
            session.new_concepts[0]
            if session.new_concepts
            else None
        )

        return SessionDigest(
            language=self.language,
            summary=self._summary(
                labels
            ),
            key_learning=self._key_learning(
                key_concept
            ),
            new_concept=new_concept,
            review=self._review(
                profile,
                key_concept,
            ),
            concept_count=len(
                concepts
            ),
            explanation_count=(
                session.explanation_count
            ),
        )


    def _label(
        self,
        concept: str,
    ) -> str:

        return (
            _LABELS[
                self.language
            ].get(
                concept,
                concept.lower(),
            )
        )


    @staticmethod
    def _choose_key_concept(
        session: LearningSession,
    ) -> str | None:

        priority = [
            "FILTER",
            "AGGREGATE",
            "DECIDE",
            "REPEAT",
            "TRANSFORM",
            "VALIDATE",
            "HANDLE ERROR",
            "LOAD DATA",
            "EXPORT",
            "DEFINE",
            "CALL",
            "RETURN",
            "MODEL",
            "IMPORT",
        ]

        for concept in priority:
            if (
                concept
                in session.concept_counts
            ):
                return concept

        concepts = list(
            session.concept_counts
        )

        return (
            concepts[0]
            if concepts
            else None
        )


    def _summary(
        self,
        labels: list[str],
    ) -> str:

        if not labels:
            return {
                "es":
                    "La sesión terminó sin conceptos detectados.",
                "en":
                    "The session ended without detected concepts.",
                "fr":
                    "La session s'est terminée sans concept détecté.",
            }[
                self.language
            ]

        if len(labels) == 1:
            joined = labels[0]

        else:
            conjunction = {
                "es": " y ",
                "en": " and ",
                "fr": " et ",
            }[
                self.language
            ]

            joined = (
                ", ".join(
                    labels[:-1]
                )
                + conjunction
                + labels[-1]
            )

        prefix = {
            "es": "Trabajaste con ",
            "en": "You worked with ",
            "fr": "Tu as travaillé avec ",
        }[
            self.language
        ]

        return (
            prefix
            + joined
            + "."
        )


    def _key_learning(
        self,
        concept: str | None,
    ) -> str:

        if concept is None:
            return {
                "es":
                    "No se detectó un concepto clave.",
                "en":
                    "No key learning concept was detected.",
                "fr":
                    "Aucun concept clé n'a été détecté.",
            }[
                self.language
            ]

        label = self._label(
            concept
        )

        prefix = {
            "es": "Enfócate en ",
            "en": "Focus on ",
            "fr": "Concentre-toi sur ",
        }[
            self.language
        ]

        return (
            prefix
            + label
            + "."
        )


    def _review(
        self,
        profile: LearningProfile,
        concept: str | None,
    ) -> str | None:

        if concept is None:
            return None

        state = (
            profile.concepts.get(
                concept
            )
        )

        if (
            state is None
            or state.status == "familiar"
        ):
            return None

        label = self._label(
            concept
        )

        templates = {
            "es":
                f"Repasa {label} en tu próxima sesión.",

            "en":
                f"Review {label} in your next session.",

            "fr":
                f"Révise {label} lors de ta prochaine session.",
        }

        return templates[
            self.language
        ]
