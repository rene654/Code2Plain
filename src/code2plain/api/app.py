from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from code2plain.service import Code2PlainService


BASE_DIR = Path(__file__).resolve().parent.parent

WEB_DIR = BASE_DIR / "web"

STATIC_DIR = WEB_DIR / "static"


class ExplainCodeRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description=(
            "Source code that Code2Plain "
            "should explain."
        ),
    )
    language: str = "es"


app = FastAPI(
    title="Code2Plain",
    version="1.0.0",
    description=(
        "Visual learning system for "
        "understanding source code."
    ),
)

service = Code2PlainService()


app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR,
    ),
    name="static",
)


@app.get("/")
def visual_learning_ui() -> FileResponse:
    return FileResponse(
        WEB_DIR / "index.html"
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "code2plain",
        "version": "1.0.0",
    }


@app.post("/v1/explain")
def explain_code(
    request: ExplainCodeRequest,
) -> dict[str, Any]:
    localized_service = Code2PlainService(
        language=request.language
    )

    return localized_service.explain_code(
        request.code
    )


# ============================================================
# LIVE LEARNING CHANNEL
# ============================================================

from code2plain.live_store import LiveExplanationStore


_live_store = LiveExplanationStore()


@app.get("/v1/live")
def get_live_explanation(
    after: int = 0,
    session_id: str = Query(
        "default",
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$",
    ),
) -> dict:
    """
    Return only an explanation newer than `after`
    for the requested live-learning session.

    Independent sessions never consume one another's
    live explanation payloads.
    """

    latest = (
        _live_store
        .latest_after(
            after,
            session_id=session_id,
        )
    )

    if latest is None:
        return {
            "changed": False,
            "version": after,
            "session_id": session_id,
        }

    return {
        "changed": True,
        **latest,
    }
