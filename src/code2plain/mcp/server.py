from __future__ import annotations

import contextlib
from typing import Any, AsyncIterator

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings as FastMCPSettings
from starlette.applications import Starlette
from starlette.routing import Mount

from code2plain.service import Code2PlainService
from code2plain.live_store import LiveExplanationStore


# MCP 1.x defines Settings as a generic BaseSettings model.
# Rebuild it explicitly before FastMCP instantiation so
# pydantic-settings sees the fully-resolved lifespan field.
FastMCPSettings.model_rebuild(
    force=True
)


mcp = FastMCP(
    "Code2Plain",
    stateless_http=True,
    json_response=True,
)

service = Code2PlainService()
live_store = LiveExplanationStore()


@mcp.tool()
def explain_code(
    code: str,
    session_id: str = "default",
    language: str = "es",
) -> dict[str, Any]:
    """
    Explain source code using Code2Plain's visual-learning model.

    session_id routes the explanation to the matching
    Code2Plain live-learning channel.

    language controls the pedagogical explanation language.
    """

    localized_service = Code2PlainService(
        language=language
    )

    result = localized_service.explain_code(
        code
    )

    live_store.publish(
        result,
        source="mcp",
        session_id=session_id,
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
