from dataclasses import dataclass

from code2plain.detection.relevance import (
    RelevantCodePart,
)


@dataclass(frozen=True)
class MicroLearningItem:
    line_number: int
    code: str
    concept: str
    explanation: str


@dataclass(frozen=True)
class MicroLearningPlan:
    total_detected: int
    items: tuple[MicroLearningItem, ...]


class MicroLearningPlanner:
    """
    Keep automatic teaching short.

    Code2Plain may detect many concepts,
    but automatic explanations should focus
    only on the most useful few.
    """

    PRIORITY = {
        "ERROR HANDLING": 100,
        "FUNCTION": 90,
        "CLASS": 90,
        "GROUP": 80,
        "AGGREGATE": 80,
        "FILTER": 75,
        "CONDITION": 70,
        "LOOP": 65,
    }

    def __init__(
        self,
        max_items: int = 3,
    ) -> None:
        self.max_items = max_items

    def build(
        self,
        parts: tuple[RelevantCodePart, ...],
    ) -> MicroLearningPlan:
        ordered = sorted(
            parts,
            key=lambda part: (
                -self.PRIORITY.get(
                    part.concept,
                    0,
                ),
                part.line_number,
            ),
        )

        selected = ordered[
            :self.max_items
        ]

        items = tuple(
            MicroLearningItem(
                line_number=part.line_number,
                code=part.code,
                concept=part.concept,
                explanation=part.explanation,
            )
            for part in selected
        )

        return MicroLearningPlan(
            total_detected=len(parts),
            items=items,
        )
