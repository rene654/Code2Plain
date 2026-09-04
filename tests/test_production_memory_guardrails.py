from pathlib import Path

from fastapi.testclient import TestClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from code2plain.api.app import app as api_app
from code2plain.deployment import (
    MAX_API_REQUEST_BYTES,
    ApiRequestBodyLimitMiddleware,
)


async def accept_request(request):
    await request.body()
    return JSONResponse(
        {"accepted": True}
    )
def make_guarded_test_app():
    inner_app = Starlette(
        routes=[
            Route(
                "/v1/test",
                accept_request,
                methods=["POST"],
            )
        ]
    )
    return ApiRequestBodyLimitMiddleware(
        inner_app,
        max_bytes=MAX_API_REQUEST_BYTES,
    )
def test_api_rejects_oversized_request_body():
    app = make_guarded_test_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/test",
            content=(
                b"x"
                * (
                    MAX_API_REQUEST_BYTES
                    + 1
                )
            ),
        )
    assert response.status_code == 413
def test_api_accepts_normal_request_body():
    app = make_guarded_test_app()
    with TestClient(app) as client:
        response = client.post(
            "/v1/test",
            content=b"normal",
        )
    assert response.status_code == 200
def test_explain_rejects_oversized_code():
    with TestClient(api_app) as client:
        response = client.post(
            "/v1/explain",
            json={
                "code":
                    "x" * 200_001,
                "language":
                    "es",
            },
        )
    assert response.status_code == 422
def test_normal_explain_still_works():
    with TestClient(api_app) as client:
        response = client.post(
            "/v1/explain",
            json={
                "code":
                    "customer = 'Acme'",
                "language":
                    "es",
            },
        )
    assert response.status_code == 200
def test_render_uses_main_with_concurrency_limit():
    render_yaml = Path(
        "render.yaml"
    ).read_text(
        encoding="utf-8"
    )
    assert "branch: main" in render_yaml
    assert "--limit-concurrency 20" in render_yaml
