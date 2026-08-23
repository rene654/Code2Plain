from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from code2plain.service import Code2PlainService
from code2plain.feedback.service import FeedbackService
from code2plain.detection.learning_pipeline import AutomaticLearningPipeline
from code2plain.detection.models import ContentCandidate
from code2plain.version import __version__


BASE_DIR = Path(__file__).resolve().parent.parent

WEB_DIR = BASE_DIR / "web"

STATIC_DIR = WEB_DIR / "static"


class AutoLearningRequest(BaseModel):
    source: str
    author_role: str
    text: str
    content_type: str = "unknown"


class GitHubFeedbackRequest(BaseModel):
    name: str
    conclusion: str
    summary: str
    details: str = ""
    file_path: str | None = None
    line: int | None = None


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
    version=__version__,
    description=(
        "Visual learning system for "
        "understanding source code."
    ),
)

service = Code2PlainService()
feedback_service = FeedbackService()
automatic_learning_pipeline = AutomaticLearningPipeline()
_latest_github_feedback: dict | None = None
_github_feedback_version = 0


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
        "version": __version__,
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

from code2plain.live_store import live_store
from code2plain.api.apple_push import router as apple_push_router


_live_store = live_store




@app.post("/v1/auto-learn")
def auto_learn(
    request: AutoLearningRequest,
) -> dict:
    result = automatic_learning_pipeline.process(
        ContentCandidate(
            source=request.source,
            author_role=request.author_role,
            text=request.text,
            content_type=request.content_type,
        )
    )

    items = []

    if result.microlearning is not None:
        items = [
            {
                "line_number": item.line_number,
                "code": item.code,
                "concept": item.concept,
                "explanation": item.explanation,
            }
            for item in result.microlearning.items
        ]

    return {
        "should_teach": result.should_teach,
        "reason": result.reason,
        "items": items,
    }


@app.post("/v1/github/feedback")
def github_feedback(
    request: GitHubFeedbackRequest,
) -> dict:
    global _latest_github_feedback
    global _github_feedback_version

    feedback = feedback_service.from_github_check(
        request.model_dump()
    )

    payload = {
        "status": feedback.status,
        "headline": feedback.headline,
        "what_failed": feedback.what_failed,
        "likely_cause": feedback.likely_cause,
        "where_to_look": feedback.where_to_look,
        "concept": feedback.concept,
    }

    _github_feedback_version += 1
    _latest_github_feedback = payload

    return {
        **payload,
        "version": _github_feedback_version,
    }


@app.get("/v1/github/feedback/latest")
def latest_github_feedback() -> dict:
    if _latest_github_feedback is None:
        return {
            "changed": False,
        }

    return {
        "changed": True,
        "version": _github_feedback_version,
        "feedback": _latest_github_feedback,
    }


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

app.include_router(apple_push_router)
