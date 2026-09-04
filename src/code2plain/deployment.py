import contextlib
from collections.abc import AsyncIterator

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount

from code2plain.api.app import app as api_app
from code2plain.mcp.server import (
    mcp,
    mcp_app,
)

MAX_API_REQUEST_BYTES = 1_000_000
class ApiRequestBodyLimitMiddleware:
    def __init__(
        self,
        app,
        *,
        max_bytes: int,
    ) -> None:
        self.app = app
        self.max_bytes = max_bytes
    async def __call__(
        self,
        scope,
        receive,
        send,
    ) -> None:
        protected = (
            scope.get("type") == "http"
            and scope.get("method")
            in {"POST", "PUT", "PATCH"}
            and scope.get("path", "")
            .startswith("/v1/")
        )
        if not protected:
            await self.app(
                scope,
                receive,
                send,
            )
            return
        headers = dict(
            scope.get("headers", [])
        )
        raw_length = headers.get(
            b"content-length"
        )
        if raw_length is not None:
            try:
                content_length = int(
                    raw_length
                )
            except ValueError:
                content_length = 0
            if (
                content_length
                > self.max_bytes
            ):
                await self._reject(
                    scope,
                    receive,
                    send,
                )
                return
        body = bytearray()
        while True:
            message = await receive()
            if (
                message.get("type")
                != "http.request"
            ):
                continue
            chunk = message.get(
                "body",
                b"",
            )
            if (
                len(body)
                + len(chunk)
                > self.max_bytes
            ):
                await self._reject(
                    scope,
                    receive,
                    send,
                )
                return
            body.extend(chunk)
            if not message.get(
                "more_body",
                False,
            ):
                break
        delivered = False
        async def replay_receive():
            nonlocal delivered
            if delivered:
                return {
                    "type": "http.request",
                    "body": b"",
                    "more_body": False,
                }
            delivered = True
            return {
                "type": "http.request",
                "body": bytes(body),
                "more_body": False,
            }
        await self.app(
            scope,
            replay_receive,
            send,
        )
    async def _reject(
        self,
        scope,
        receive,
        send,
    ) -> None:
        response = JSONResponse(
            {
                "detail":
                    "Request body too large."
            },
            status_code=413,
        )
        await response(
            scope,
            receive,
            send,
        )
@contextlib.asynccontextmanager
async def lifespan(
    app: Starlette,
) -> AsyncIterator[None]:
    async with mcp.session_manager.run():
        yield
app = Starlette(
    routes=[
        Mount(
            "/mcp",
            app=mcp_app,
        ),
        Mount(
            "/",
            app=api_app,
        ),
    ],
    lifespan=lifespan,
)
app.add_middleware(
    ApiRequestBodyLimitMiddleware,
    max_bytes=MAX_API_REQUEST_BYTES,
)
