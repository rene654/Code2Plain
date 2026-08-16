from __future__ import annotations

from dataclasses import dataclass

from code2plain.learning.digest import (
    SessionDigest,
    SessionDigestBuilder,
)
from code2plain.learning.models import (
    LearningConceptState,
    LearningProfile,
    LearningSession,
)


# Pedagogical importance.
#
# This is NOT code complexity.
# It represents how useful a concept generally is to surface
# while somebody is learning programming.

_CONCEPT_WEIGHT = {
    "HANDLE ERROR": 100,
    "DECIDE": 95,
    "FILTER": 90,
    "AGGREGATE": 88,
    "TRANSFORM": 85,
    "REPEAT": 84,
    "VALIDATE": 82,
    "DEFINE": 75,
    "MODEL": 75,
    "LOAD DATA": 55,
    "EXPORT": 50,
    "CALL": 45,
    "RETURN": 40,
    "IMPORT": 10,
}


_STATUS_WEIGHT = {
    "new": 30,
    "practicing": 20,
    "familiar": -50,
}


@dataclass(frozen=True)
class AdaptiveSessionDigest(
    SessionDigest
):
    focus_concept: str | None
    focus_status: str | None
    focus_score: int
    focus_reason: str
    reinforcement: str | None


class AdaptiveSessionDigestBuilder(
    SessionDigestBuilder
):
    """
    Builds a digest using the learner's historical profile.

    Automation-first rule:

    Code2Plain decides what deserves attention.
    The user does not need to ask what to review.
    """

    def build(
        self,
        session: LearningSession,
        profile: LearningProfile,
    ) -> AdaptiveSessionDigest:

        concepts = list(
            session.concept_counts
        )

        labels = [
            self._label(
                concept
            )
            for concept in concepts
        ]

        focus_concept = (
            self._choose_adaptive_focus(
                session,
                profile,
            )
        )

        state = (
            profile.concepts.get(
                focus_concept
            )
            if focus_concept
            else None
        )

        score = (
            self._score(
                focus_concept,
                state,
            )
            if focus_concept
            else 0
        )

        new_concept = (
            self._best_new_concept(
                session,
                profile,
            )
        )

        return AdaptiveSessionDigest(
            language=self.language,

            summary=self._summary(
                labels
            ),

            key_learning=(
                self._adaptive_key_learning(
                    focus_concept,
                    state,
                )
            ),

            new_concept=new_concept,

            review=(
                self._adaptive_review(
                    focus_concept,
                    state,
                )
            ),

            concept_count=len(
                concepts
            ),

            explanation_count=(
                session.explanation_count
            ),

            focus_concept=focus_concept,

            focus_status=(
                state.status
                if state
                else None
            ),

            focus_score=score,

            focus_reason=(
                self._focus_reason(
                    focus_concept,
                    state,
                )
            ),

            reinforcement=(
                self._reinforcement(
                    focus_concept,
                    state,
                )
            ),
        )


    def _choose_adaptive_focus(
        self,
        session: LearningSession,
        profile: LearningProfile,
    ) -> str | None:

        concepts = list(
            session.concept_counts
        )

        if not concepts:
            return None

        return max(
            concepts,
            key=lambda concept:
                self._score(
                    concept,
                    profile.concepts.get(
                        concept
                    ),
                ),
        )


    @staticmethod
    def _score(
        concept: str | None,
        state: LearningConceptState | None,
    ) -> int:

        if concept is None:
            return 0

        base = (
            _CONCEPT_WEIGHT.get(
                concept,
                60,
            )
        )

        status = (
            state.status
            if state
            else "new"
        )

        score = (
            base
            + _STATUS_WEIGHT.get(
                status,
                0,
            )
        )

        # A concept repeatedly seen but not yet familiar is
        # especially valuable to reinforce.
        if (
            state
            and state.status == "practicing"
        ):
            score += min(
                state.total_exposures,
                4,
            )

        return score


    def _best_new_concept(
        self,
        session: LearningSession,
        profile: LearningProfile,
    ) -> str | None:

        candidates = [
            concept
            for concept
            in session.new_concepts
            if concept
            in session.concept_counts
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda concept:
                self._score(
                    concept,
                    profile.concepts.get(
                        concept
                    ),
                ),
        )


    def _adaptive_key_learning(
        self,
        concept: str | None,
        state: LearningConceptState | None,
    ) -> str:

        if concept is None:
            return {
                "es":
                    "No se detectó un aprendizaje prioritario.",
                "en":
                    "No priority learning concept was detected.",
                "fr":
                    "Aucun apprentissage prioritaire détecté.",
            }[
                self.language
            ]

        label = self._label(
            concept
        )

        status = (
            state.status
            if state
            else "new"
        )

        if self.language == "en":

            if status == "new":
                return (
                    f"Pay attention to {label}: "
                    "this is new in your learning history."
                )

            if status == "practicing":
                return (
                    f"Reinforce {label}: "
                    "you are still consolidating it."
                )

            return (
                f"Use {label} as a bridge "
                "to more advanced concepts."
            )


        if self.language == "fr":

            if status == "new":
                return (
                    f"Observe bien {label} : "
                    "c'est nouveau dans ton parcours."
                )

            if status == "practicing":
                return (
                    f"Renforce {label} : "
                    "tu es encore en train de le consolider."
                )

            return (
                f"Utilise {label} comme base "
                "pour des concepts plus avancés."
            )


        if status == "new":
            return (
                f"Pon atención a {label}: "
                "es nuevo en tu historial de aprendizaje."
            )

        if status == "practicing":
            return (
                f"Refuerza {label}: "
                "todavía lo estás consolidando."
            )

        return (
            f"Usa {label} como base "
            "para conectar conceptos más avanzados."
        )


    def _focus_reason(
        self,
        concept: str | None,
        state: LearningConceptState | None,
    ) -> str:

        if concept is None:
            return ""

        label = self._label(
            concept
        )

        status = (
            state.status
            if state
            else "new"
        )

        exposures = (
            state.total_exposures
            if state
            else 1
        )

        if self.language == "en":
            return (
                f"{label} was selected because it is "
                f"{status} after {exposures} exposure(s)."
            )

        if self.language == "fr":
            return (
                f"{label} a été sélectionné car son état est "
                f"{status} après {exposures} exposition(s)."
            )

        return (
            f"{label} fue seleccionado porque está en estado "
            f"{status} después de {exposures} exposición(es)."
        )


    def _adaptive_review(
        self,
        concept: str | None,
        state: LearningConceptState | None,
    ) -> str | None:

        if (
            concept is None
            or state is None
        ):
            return None

        if state.status == "familiar":
            return None

        label = self._label(
            concept
        )

        if self.language == "en":
            return (
                f"Review {label} in your next coding session."
            )

        if self.language == "fr":
            return (
                f"Révise {label} lors de ta prochaine session."
            )

        return (
            f"Repasa {label} en tu próxima sesión de código."
        )


    def _reinforcement(
        self,
        concept: str | None,
        state: LearningConceptState | None,
    ) -> str | None:

        if (
            concept is None
            or state is None
        ):
            return None

        label = self._label(
            concept
        )

        if state.status == "new":

            if self.language == "en":
                return (
                    f"Notice where {label} appears "
                    "the next time AI generates code."
                )

            if self.language == "fr":
                return (
                    f"Repère où apparaît {label} "
                    "la prochaine fois que l'IA génère du code."
                )

            return (
                f"Observa dónde aparece {label} "
                "la próxima vez que la IA genere código."
            )


        if state.status == "practicing":

            if self.language == "en":
                return (
                    f"Try to predict what {label} will do "
                    "before reading the explanation."
                )

            if self.language == "fr":
                return (
                    f"Essaie de prévoir ce que fera {label} "
                    "avant de lire l'explication."
                )

            return (
                f"Intenta predecir qué hará {label} "
                "antes de leer la explicación."
            )


        return None
