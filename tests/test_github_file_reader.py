import base64

import httpx

from code2plain.github_file_reader import (
    GitHubFileReader,
)


def test_read_public_github_file():
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "content":
                    base64.b64encode(
                        b'print("hello")'
                    ).decode(),
            },
        )

    reader = GitHubFileReader(
        client=httpx.Client(
            transport=httpx.MockTransport(
                handler
            )
        )
    )

    result = reader.read_url(
        "https://github.com/"
        "ReneCru/Code2Plain/blob/"
        "main/example.py"
    )

    assert result.owner == "ReneCru"
    assert result.repo == "Code2Plain"
    assert result.path == "example.py"
    assert result.content == 'print("hello")'
