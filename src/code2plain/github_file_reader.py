import base64
import re
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class GitHubFile:
    owner: str
    repo: str
    ref: str
    path: str
    content: str


class GitHubFileReader:
    """
    Read a public GitHub file from a normal github.com URL.
    """

    PATTERN = re.compile(
        r"^https://github\.com/"
        r"(?P<owner>[^/]+)/"
        r"(?P<repo>[^/]+)/blob/"
        r"(?P<ref>[^/]+)/"
        r"(?P<path>.+)$"
    )

    def __init__(
        self,
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client(
            timeout=15.0
        )

    def read_url(
        self,
        url: str,
    ) -> GitHubFile:
        match = self.PATTERN.match(
            url.strip()
        )

        if not match:
            raise ValueError(
                "GitHub file URL is not valid."
            )

        data = match.groupdict()

        response = self._client.get(
            (
                "https://api.github.com/repos/"
                f"{data['owner']}/"
                f"{data['repo']}/contents/"
                f"{data['path']}"
            ),
            params={
                "ref": data["ref"],
            },
            headers={
                "Accept":
                    "application/vnd.github+json",
            },
        )

        response.raise_for_status()

        payload = response.json()

        encoded = payload.get(
            "content",
            "",
        )

        content = base64.b64decode(
            encoded
        ).decode(
            "utf-8"
        )

        return GitHubFile(
            owner=data["owner"],
            repo=data["repo"],
            ref=data["ref"],
            path=data["path"],
            content=content,
        )
