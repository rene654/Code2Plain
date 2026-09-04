from dataclasses import dataclass
from typing import Any

from code2plain.feedback.models import CheckFailure


@dataclass(frozen=True)
class GitHubCheckPayload:
    name: str
    conclusion: str
    summary: str
    details: str = ""
    file_path: str | None = None
    line: int | None = None


class GitHubFeedbackAdapter:
    """
    Normalize GitHub-style check results into Code2Plain's
    provider-neutral CheckFailure model.
    """

    def normalize_check(
        self,
        payload: GitHubCheckPayload,
    ) -> CheckFailure:
        return CheckFailure(
            name=payload.name.strip(),
            conclusion=payload.conclusion.strip(),
            summary=payload.summary.strip(),
            details=payload.details.strip(),
            file_path=(
                payload.file_path.strip()
                if payload.file_path
                else None
            ),
            line=payload.line,
        )

    def normalize_dict(
        self,
        payload: dict[str, Any],
    ) -> CheckFailure:
        return self.normalize_check(
            GitHubCheckPayload(
                name=str(
                    payload.get("name", "")
                ),
                conclusion=str(
                    payload.get("conclusion", "")
                ),
                summary=str(
                    payload.get("summary", "")
                ),
                details=str(
                    payload.get("details", "")
                ),
                file_path=(
                    str(payload["file_path"])
                    if payload.get("file_path")
                    else None
                ),
                line=(
                    int(payload["line"])
                    if payload.get("line") is not None
                    else None
                ),
            )
        )
