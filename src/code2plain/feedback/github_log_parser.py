import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedFailureLog:
    summary: str
    file_path: str | None = None
    line: int | None = None
    details: str = ""


class GitHubFailureLogParser:
    """
    Extract only the useful failure context
    from a GitHub Actions log.
    """

    def parse(
        self,
        log: str,
    ) -> ParsedFailureLog:
        file_path = None
        line = None

        location = re.search(
            r"(tests/[^\s:]+\.py):(\d+):\s*([^\n]+)",
            log,
        )

        if location:
            file_path = location.group(1)
            line = int(location.group(2))

        failed = re.search(
            r"FAILED\s+([^\n]+)",
            log,
        )

        summary = (
            failed.group(1).strip()
            if failed
            else "GitHub check failed"
        )

        assertion = re.search(
            r"E\s+(assert .+)",
            log,
        )

        details = (
            assertion.group(1).strip()
            if assertion
            else ""
        )

        return ParsedFailureLog(
            summary=summary,
            file_path=file_path,
            line=line,
            details=details,
        )
