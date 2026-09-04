import contextlib
from typing import AsyncIterator

from starlette.applications import Starlette
from starlette.routing import Mount

from code2plain.api.app import app as api_app
from code2plain.mcp.server import (
    mcp,
    mcp_app,
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
