from fastapi.testclient import TestClient

import code2plain.api.app as api_module
import code2plain.mcp.server as mcp_module
from code2plain.api.app import app


client = TestClient(app)


def test_api_and_mcp_share_live_store():

    assert (
        api_module._live_store
        is mcp_module.live_store
    )


def test_mcp_publication_reaches_live_api():

    session_id = (
        "frontend_live_regression"
    )

    result = mcp_module.explain_code(
        code=(
            "numbers = [1, 2, 3]\n"
            "total = sum(numbers)"
        ),
        session_id=session_id,
        language="es",
    )

    assert result["sections"]

    response = client.get(
        "/v1/live",
        params={
            "after": 0,
            "session_id": session_id,
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["changed"] is True
    assert payload["session_id"] == session_id
