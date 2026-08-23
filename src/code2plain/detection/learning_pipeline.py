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
from code2plain.detection.microlearning import (
    MicroLearningPlan,
    MicroLearningPlanner,
)


@dataclass(frozen=True)
class LearningDetectionResult:
    should_teach: bool
    reason: str
    code: str
    learning_points: tuple[RelevantCodePart, ...]
    microlearning: MicroLearningPlan | None = None


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
        microlearning_planner: MicroLearningPlanner | None = None,
    ) -> None:
        self.detection_pipeline = (
            detection_pipeline
            or DetectionPipeline()
        )
        self.relevance_engine = (
            relevance_engine
            or CodeRelevanceEngine()
        )
        self.microlearning_planner = (
            microlearning_planner
            or MicroLearningPlanner()
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

        plan = self.microlearning_planner.build(
            points
        )

        return LearningDetectionResult(
            should_teach=True,
            reason="relevant_new_ai_code",
            code=detection.code,
            learning_points=points,
            microlearning=plan,
        )
