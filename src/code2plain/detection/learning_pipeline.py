from dataclasses import dataclass

from code2plain.detection.models import (
    ContentCandidate,
)
from code2plain.detection.pipeline import (
    DetectionPipeline,
)
from code2plain.detection.relevance import (
    CodeRelevanceEngine,
    RelevantCodePart,
)


@dataclass(frozen=True)
class LearningDetectionResult:
    should_teach: bool
    reason: str
    code: str
    learning_points: tuple[RelevantCodePart, ...]


class AutomaticLearningPipeline:
    """
    Complete automatic-learning decision:

    AI code
        -> new code
        -> relevant concepts
        -> teach only useful parts
    """

    def __init__(
        self,
        detection_pipeline: DetectionPipeline | None = None,
        relevance_engine: CodeRelevanceEngine | None = None,
    ) -> None:
        self.detection_pipeline = (
            detection_pipeline
            or DetectionPipeline()
        )
        self.relevance_engine = (
            relevance_engine
            or CodeRelevanceEngine()
        )

    def process(
        self,
        candidate: ContentCandidate,
    ) -> LearningDetectionResult:
        detection = (
            self.detection_pipeline
            .process(candidate)
        )

        if not detection.should_explain:
            return LearningDetectionResult(
                should_teach=False,
                reason=detection.reason,
                code=detection.code,
                learning_points=(),
            )

        points = tuple(
            self.relevance_engine.analyze(
                detection.code
            )
        )

        if not points:
            return LearningDetectionResult(
                should_teach=False,
                reason="no_relevant_learning_points",
                code=detection.code,
                learning_points=(),
            )

        return LearningDetectionResult(
            should_teach=True,
            reason="relevant_new_ai_code",
            code=detection.code,
            learning_points=points,
        )
