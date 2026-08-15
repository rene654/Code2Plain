from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from code2plain.service import Code2PlainService


class ExplainCodeRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="Source code that Code2Plain should explain.",
    )


app = FastAPI(
    title="Code2Plain API",
    version="0.1.0",
    description=(
        "Transforms source code into structured "
        "visual-learning explanations."
    ),
)

service = Code2PlainService()


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
    return service.explain_code(request.code)
