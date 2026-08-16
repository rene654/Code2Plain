from __future__ import annotations

import contextlib
from typing import Any, AsyncIterator

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

from code2plain.service import Code2PlainService
from code2plain.live_store import LiveExplanationStore


mcp = FastMCP(
    "Code2Plain",
    stateless_http=True,
    json_response=True,
)

service = Code2PlainService()
live_store = LiveExplanationStore()


@mcp.tool()
def explain_code(code: str) -> dict[str, Any]:
    """
    Explain source code using Code2Plain's visual-learning model.
    """
    result = service.explain_code(code)

    live_store.publish(
        result,
        source="mcp",
    )

    return result


mcp_app = mcp.streamable_http_app()


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Mount("/", app=mcp_app),
    ],
    lifespan=lifespan,
)
