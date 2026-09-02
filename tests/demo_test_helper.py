from uuid import uuid4

from fastapi.testclient import TestClient


def demo_credentials(
    client: TestClient,
    user_id: str | None = None,
) -> tuple[str, str]:
    """
    Creates legitimate demo credentials for API tests.

    Production security remains unchanged:
    tests must enter protected learning endpoints
    through the same demo-access contract as users.
    """

    resolved_user_id = (
        user_id
        or "test-demo-" + uuid4().hex
    )

    response = client.post(
        "/v1/demo/start",
        json={
            "user_id":
                resolved_user_id,
        },
    )

    assert response.status_code == 200

    token = response.json()["token"]

    return (
        resolved_user_id,
        token,
    )
