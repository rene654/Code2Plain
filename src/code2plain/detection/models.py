from dataclasses import dataclass


@dataclass(frozen=True)
class ContentCandidate:
    """
    A piece of content observed by a future source adapter.

    The detector does not inspect arbitrary screens.
    Adapters provide structured context about where
    the content came from.
    """

    source: str
    author_role: str
    text: str
    content_type: str = "unknown"


@dataclass(frozen=True)
class DetectionResult:
    should_explain: bool
    confidence: float
    reason: str
    code: str = ""
