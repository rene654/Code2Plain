from __future__ import annotations

import contextlib
from typing import Any, AsyncIterator

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings as FastMCPSettings
from starlette.applications import Starlette
from starlette.routing import Mount

from code2plain.service import Code2PlainService
from code2plain.live_store import live_store
from code2plain.line_learning import line_by_line_explainer
from code2plain.detection.learning_pipeline import (
    AutomaticLearningPipeline,
)
from code2plain.detection.models import (
    ContentCandidate,
)
from code2plain.detection.confidence import (
    ExplanationConfidenceAssessor,
)


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
    streamable_http_path="/",
)

service = Code2PlainService()


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



@mcp.tool()
def learn_code(
    code: str,
    language: str = "es",
) -> dict[str, Any]:
    """
    Teach the most important concepts in AI-generated code.

    Returns a compact learning layer instead of explaining
    every line.
    """

    pipeline = AutomaticLearningPipeline()

    result = pipeline.process(
        ContentCandidate(
            source="chatgpt",
            author_role="assistant",
            content_type="code",
            text=code,
        )
    )

    if (
        not result.should_teach
        or result.microlearning is None
    ):
        return {
            "should_teach": False,
            "items": [],
        }

    assessor = ExplanationConfidenceAssessor()

    items = []

    for item in result.microlearning.items:
        confidence = assessor.assess(
            code=code,
            line_number=item.line_number,
            concept=item.concept,
        )

        items.append(
            {
                "line_number":
                    item.line_number,
                "code":
                    item.code,
                "concept":
                    item.concept,
                "explanation":
                    item.explanation,
                "confidence":
                    confidence.score,
                "context_status":
                    confidence.status,
            }
        )

    return {
        "should_teach": True,
        "total_detected":
            result.microlearning.total_detected,
        "items": items,
        "language": language,
    }



@mcp.tool()
def explain_line_by_line(
    code: str,
    language: str = "es",
) -> dict[str, Any]:
    """
    Explain code line by line in execution order.

    Important operations receive concept labels
    and confidence while simple lines receive
    compact explanations.
    """

    items = line_by_line_explainer.explain(
        code
    )

    return {
        "total_lines":
            len(code.splitlines()),
        "explained_lines":
            len(items),
        "language":
            language,
        "items": [
            {
                "line_number":
                    item.line_number,
                "code":
                    item.code,
                "explanation":
                    item.explanation,
                "concept":
                    item.concept,
                "key":
                    item.key,
                "confidence":
                    item.confidence,
                "context_status":
                    item.context_status,
            }
            for item in items
        ],
    }


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
