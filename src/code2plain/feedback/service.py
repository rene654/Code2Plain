from typing import Any

from code2plain.adapters.github_feedback import (
    GitHubFeedbackAdapter,
)
from code2plain.feedback.analyzer import (
    FailureAnalyzer,
)
from code2plain.feedback.models import (
    LearningFeedback,
)


class FeedbackService:
    """
    Small application service for converting external
    CI/check results into Code2Plain learning feedback.
    """

    def __init__(
        self,
        github_adapter: GitHubFeedbackAdapter | None = None,
        analyzer: FailureAnalyzer | None = None,
    ) -> None:
        self.github_adapter = (
            github_adapter
            or GitHubFeedbackAdapter()
        )
        self.analyzer = (
            analyzer
            or FailureAnalyzer()
        )

    def from_github_check(
        self,
        payload: dict[str, Any],
    ) -> LearningFeedback:
        failure = (
            self.github_adapter
            .normalize_dict(payload)
        )

        return self.analyzer.analyze(
            failure
        )
