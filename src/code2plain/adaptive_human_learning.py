from __future__ import annotations

from dataclasses import dataclass

from code2plain.human_skill_detection import (
    human_skill_detector,
)
from code2plain.human_skill_memory import (
    HumanSkillMemoryStore,
    human_skill_memory,
)
from code2plain.human_skills import (
    get_human_skill,
)
from code2plain.learning_motivation import (
    LearningMotivationEngine,
    learning_motivation,
)


@dataclass(frozen=True)
class HumanLearningFeedback:
    skill_id: str
    skill_name: str
    simple_meaning: str
    mastery_level: str
    seen: int
    correct: int
    incorrect: int
    mastery: float
    message: str
    next_step: str


class AdaptiveHumanLearningEngine:
    """
    Converts transient code analysis into persistent
    abstract learning progress.

    Source code is never written to persistent memory.
    """

    def __init__(
        self,
        *,
        memory: HumanSkillMemoryStore | None = None,
        motivation: LearningMotivationEngine | None = None,
    ) -> None:
        self.memory = (
            memory
            if memory is not None
            else human_skill_memory
        )

        self.motivation = (
            motivation
            if motivation is not None
            else learning_motivation
        )

    def record_answer(
        self,
        *,
        user_id: str,
        skill_id: str,
        correct: bool,
    ) -> HumanLearningFeedback:
        skill = get_human_skill(
            skill_id
        )

        if skill is None:
            raise ValueError(
                "Unknown human skill."
            )

        progress = self.memory.record_answer(
            user_id=user_id,
            skill_id=skill_id,
            correct=correct,
        )

        feedback = self.motivation.build(
            skill_name=skill.name,
            seen=progress.seen,
            correct=progress.correct,
            incorrect=progress.incorrect,
        )

        return HumanLearningFeedback(
            skill_id=skill.skill_id,
            skill_name=skill.name,
            simple_meaning=(
                skill.simple_meaning
            ),
            mastery_level=(
                feedback.mastery_level
            ),
            seen=progress.seen,
            correct=progress.correct,
            incorrect=progress.incorrect,
            mastery=progress.mastery,
            message=feedback.message,
            next_step=feedback.next_step,
        )


    def observe_code(
        self,
        *,
        user_id: str,
        code: str,
    ) -> list[HumanLearningFeedback]:
        skill_ids = (
            human_skill_detector.detect(
                code
            )
        )

        results = []

        for skill_id in skill_ids:
            skill = get_human_skill(
                skill_id
            )

            if skill is None:
                continue

            progress = self.memory.record_seen(
                user_id=user_id,
                skill_id=skill_id,
            )

            feedback = self.motivation.build(
                skill_name=skill.name,
                seen=progress.seen,
                correct=progress.correct,
                incorrect=progress.incorrect,
            )

            results.append(
                HumanLearningFeedback(
                    skill_id=skill.skill_id,
                    skill_name=skill.name,
                    simple_meaning=(
                        skill.simple_meaning
                    ),
                    mastery_level=(
                        feedback.mastery_level
                    ),
                    seen=progress.seen,
                    correct=progress.correct,
                    incorrect=progress.incorrect,
                    mastery=progress.mastery,
                    message=feedback.message,
                    next_step=feedback.next_step,
                )
            )

        return results


adaptive_human_learning = (
    AdaptiveHumanLearningEngine()
)
