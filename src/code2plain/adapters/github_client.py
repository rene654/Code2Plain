from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class GitHubCheckRun:
    id: int
    name: str
    conclusion: str | None
    summary: str
    details: str
    details_url: str = ""


class GitHubClient:
    """
    Minimal read-only GitHub API client.
    """

    def __init__(
        self,
        token: str,
        client: httpx.Client | None = None,
    ) -> None:
        if not token.strip():
            raise ValueError(
                "GitHub token cannot be empty"
            )

        self._client = (
            client
            or httpx.Client(
                base_url="https://api.github.com",
                timeout=10.0,
                headers={
                    "Accept":
                        "application/vnd.github+json",
                    "Authorization":
                        f"Bearer {token}",
                    "X-GitHub-Api-Version":
                        "2022-11-28",
                },
            )
        )

    def get_check_runs(
        self,
        owner: str,
        repo: str,
        ref: str,
    ) -> list[GitHubCheckRun]:
        response = self._client.get(
            f"/repos/{owner}/{repo}/commits/{ref}/check-runs"
        )

        response.raise_for_status()

        payload = response.json()

        results = []

        for item in payload.get(
            "check_runs",
            [],
        ):
            output = item.get("output") or {}

            results.append(
                GitHubCheckRun(
                    id=int(item["id"]),
                    name=str(
                        item.get("name", "")
                    ),
                    conclusion=(
                        str(item["conclusion"])
                        if item.get("conclusion")
                        is not None
                        else None
                    ),
                    summary=str(
                        output.get(
                            "summary",
                            "",
                        )
                        or ""
                    ),
                    details=str(
                        output.get(
                            "text",
                            "",
                        )
                        or ""
                    ),
                    details_url=str(
                        item.get(
                            "details_url",
                            "",
                        )
                        or ""
                    ),
                )
            )

        return results

    def get_failed_checks(
        self,
        owner: str,
        repo: str,
        ref: str,
    ) -> list[GitHubCheckRun]:
        return [
            check
            for check in self.get_check_runs(
                owner,
                repo,
                ref,
            )
            if check.conclusion
            in {
                "failure",
                "timed_out",
                "cancelled",
                "action_required",
            }
        ]


    def get_check_log(
        self,
        owner: str,
        repo: str,
        check: GitHubCheckRun,
    ) -> str:
        """
        Read the GitHub Actions job log associated
        with a check run when available.
        """
        import re

        match = re.search(
            r"/job/(\d+)",
            check.details_url,
        )

        if not match:
            return ""

        job_id = match.group(1)

        response = self._client.get(
            (
                f"/repos/{owner}/{repo}"
                f"/actions/jobs/{job_id}/logs"
            ),
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.text
