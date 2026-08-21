from dataclasses import dataclass


@dataclass(frozen=True)
class CheckFailure:
    """
    Normalized failure received from an external CI/check provider.

    Code2Plain does not execute the user's code.
    It receives and interprets an existing failure result.
    """

    name: str
    conclusion: str
    summary: str
    details: str = ""
    file_path: str | None = None
    line: int | None = None


@dataclass(frozen=True)
class LearningFeedback:
    """
    Compact learning response shown to the user.

    Intentionally small: Code2Plain should explain only
    what is useful for understanding and correcting the failure.
    """

    status: str
    headline: str
    what_failed: str
    likely_cause: str
    where_to_look: str
    concept: str
