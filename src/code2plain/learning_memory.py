from dataclasses import dataclass, field


@dataclass
class ConceptProgress:
    seen: int = 0
    correct: int = 0
    incorrect: int = 0


@dataclass
class LearningProfile:
    concepts: dict[str, ConceptProgress] = field(
        default_factory=dict
    )


class LearningMemory:
    """
    Minimal in-memory learning profile for MVP use.

    Tracks:
    - how often a concept was seen
    - correct answers
    - incorrect answers
    """

    def __init__(self) -> None:
        self.profile = LearningProfile()

    def seen(
        self,
        concept: str,
    ) -> ConceptProgress:
        progress = self.profile.concepts.setdefault(
            concept,
            ConceptProgress(),
        )

        progress.seen += 1

        return progress

    def answer(
        self,
        concept: str,
        *,
        correct: bool,
    ) -> ConceptProgress:
        progress = self.profile.concepts.setdefault(
            concept,
            ConceptProgress(),
        )

        if correct:
            progress.correct += 1
        else:
            progress.incorrect += 1

        return progress

    def level(
        self,
        concept: str,
    ) -> str:
        progress = self.profile.concepts.get(
            concept
        )

        if progress is None:
            return "nuevo"

        total_answers = (
            progress.correct
            + progress.incorrect
        )

        if total_answers == 0:
            return "en aprendizaje"

        accuracy = (
            progress.correct
            / total_answers
        )

        if (
            total_answers >= 3
            and accuracy >= 0.80
        ):
            return "dominado"

        if accuracy < 0.60:
            return "reforzar"

        return "en aprendizaje"


learning_memory = LearningMemory()
