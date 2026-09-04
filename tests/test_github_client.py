import httpx

from code2plain.adapters.github_client import (
    GitHubClient,
)


def test_github_client_reads_failed_checks():
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        assert request.url.path == (
            "/repos/rene654/Code2Plain/"
            "commits/main/check-runs"
        )

        return httpx.Response(
            200,
            json={
                "check_runs": [
                    {
                        "id": 10,
                        "name": "pytest",
                        "conclusion": "failure",
                        "output": {
                            "summary":
                                "2 tests failed",
                            "text":
                                "AssertionError",
                        },
                    },
                    {
                        "id": 11,
                        "name": "lint",
                        "conclusion": "success",
                        "output": {
                            "summary": "Passed",
                            "text": "",
                        },
                    },
                ]
            },
        )

    transport = httpx.MockTransport(
        handler
    )

    http_client = httpx.Client(
        base_url="https://api.github.com",
        transport=transport,
    )

    client = GitHubClient(
        token="test-token",
        client=http_client,
    )

    failed = client.get_failed_checks(
        "rene654",
        "Code2Plain",
        "main",
    )

    assert len(failed) == 1
    assert failed[0].name == "pytest"
    assert failed[0].summary == (
        "2 tests failed"
    )


def test_github_token_cannot_be_empty():
    try:
        GitHubClient(token="")
    except ValueError as error:
        assert "cannot be empty" in str(
            error
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )
