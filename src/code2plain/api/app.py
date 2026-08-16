from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
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


app = FastAPI(
    title="Code2Plain",
    version="0.1.0",
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
        "version": "0.1.0",
    }


@app.post("/v1/explain")
def explain_code(
    request: ExplainCodeRequest,
) -> dict[str, Any]:
    return service.explain_code(
        request.code
    )
