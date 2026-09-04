from code2plain.detection.delta import (
    CodeDeltaTracker,
)
from code2plain.detection.detector import (
    AICodeDetector,
)
from code2plain.detection.models import (
    ContentCandidate,
    DetectionResult,
)


class DetectionPipeline:
    """
    Conservative automatic-learning gate.

    AI source
        -> code detected
        -> new delta
        -> explain
    """

    def __init__(
        self,
        detector: AICodeDetector | None = None,
        delta_tracker: CodeDeltaTracker | None = None,
    ) -> None:
        self.detector = detector or AICodeDetector()
        self.delta_tracker = (
            delta_tracker or CodeDeltaTracker()
        )

    def process(
        self,
        candidate: ContentCandidate,
    ) -> DetectionResult:
        result = self.detector.detect(
            candidate
        )

        if not result.should_explain:
            return result

        delta = self.delta_tracker.check(
            result.code
        )

        if not delta.is_new:
            return DetectionResult(
                should_explain=False,
                confidence=result.confidence,
                reason="already_seen",
                code=result.code,
            )

        return result
