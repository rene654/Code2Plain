from dataclasses import dataclass
from typing import Any


FORBIDDEN_PERSISTENT_FIELDS = {
    "code",
    "source_code",
    "snippet",
    "raw_code",
    "content",
    "text",
}


@dataclass(frozen=True)
class LearningConceptRecord:
    concept: str
    seen: int = 0
    correct: int = 0
    incorrect: int = 0


class LearningPrivacyBoundary:
    """
    Privacy boundary for persistent learning memory.

    Code2Plain may remember abstract learning concepts and
    progress. Source code must never cross this boundary.
    """

    def validate_concept(
        self,
        concept: str,
    ) -> str:
        concept = concept.strip()

        if not concept:
            raise ValueError(
                "Learning concept cannot be empty."
            )

        if "\n" in concept:
            raise ValueError(
                "Learning memory accepts concepts only."
            )

        if len(concept) > 80:
            raise ValueError(
                "Learning concept is too long."
            )

        return concept

    def validate_payload(
        self,
        payload: dict[str, Any],
    ) -> None:
        forbidden = (
            FORBIDDEN_PERSISTENT_FIELDS
            & set(payload)
        )

        if forbidden:
            names = ", ".join(
                sorted(forbidden)
            )

            raise ValueError(
                "Source material cannot be persisted "
                f"in learning memory: {names}"
            )


learning_privacy_boundary = (
    LearningPrivacyBoundary()
)
