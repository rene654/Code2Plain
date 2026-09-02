from __future__ import annotations

from code2plain.web.app import router as web_router

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from code2plain.service import Code2PlainService
from code2plain.feedback.service import FeedbackService
from code2plain.detection.learning_pipeline import AutomaticLearningPipeline
from code2plain.detection.models import ContentCandidate
from code2plain.detection.confidence import ExplanationConfidenceAssessor
from code2plain.learning_interaction import LearningInteractionBuilder
from code2plain.learning_memory import learning_memory
from code2plain.learning_memory_store import learning_memory_store
from code2plain.adaptive_learning import AdaptiveLearningEngine
from code2plain.line_learning import line_by_line_explainer
from code2plain.context_learning import context_aware_teaching
from code2plain.block_teaching import context_block_teaching
from code2plain.adaptive_human_learning import adaptive_human_learning
from code2plain.human_skill_detection import (
    primary_human_skill,
)
from code2plain.human_skills import (
    get_human_skill,
)
from code2plain.learning_checks import (
    learning_check_engine,
)
from code2plain.adaptive_teaching_policy import (
    adaptive_teaching_policy,
)
from code2plain.human_skill_memory import (
    human_skill_memory,
)
from code2plain.github_file_reader import GitHubFileReader
from code2plain.version import __version__


BASE_DIR = Path(__file__).resolve().parent.parent

WEB_DIR = BASE_DIR / "web"

STATIC_DIR = WEB_DIR / "static"


class AutoLearningRequest(BaseModel):
    source: str
    author_role: str
    text: str
    content_type: str = "unknown"


class GitHubFileLearnRequest(BaseModel):
    url: str = Field(
        min_length=10,
        max_length=2000,
    )


class LearningCheckAnswerRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=128,
    )
    skill_id: str = Field(
        min_length=1,
        max_length=80,
    )
    code: str = Field(
        min_length=1,
    )
    input_from: str | None = None
    output_to: str | None = None
    selected_index: int = Field(
        ge=0,
        le=10,
    )


class HumanLearningAnswerRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=128,
    )
    skill_id: str = Field(
        min_length=1,
        max_length=80,
    )
    correct: bool


class LineByLineRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=200_000,
    )
    user_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=128,
    )


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
explanation_confidence = ExplanationConfidenceAssessor()
learning_interaction = LearningInteractionBuilder()
adaptive_learning = AdaptiveLearningEngine()
github_file_reader = GitHubFileReader()
_latest_github_feedback: dict | None = None
_github_feedback_version = 0


app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR,
    ),
    name="static",
)


app.include_router(web_router)


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
        items = []

        for item in result.microlearning.items:
            confidence = explanation_confidence.assess(
                code=result.code,
                line_number=item.line_number,
                concept=item.concept,
            )

            interaction = learning_interaction.build(
                item.concept
            )

            progress = learning_memory.seen(
                item.concept
            )

            learning_memory_store.record_seen(
                item.concept
            )

            level = learning_memory.level(
                item.concept
            )

            adaptive = adaptive_learning.adapt(
                concept=item.concept,
                explanation=item.explanation,
                challenge=interaction.challenge,
                level=level,
            )

            items.append(
                {
                    "line_number": item.line_number,
                    "code": item.code,
                    "concept": item.concept,
                    "explanation": adaptive.explanation,
                    "why": interaction.why,
                    "challenge": adaptive.challenge,
                    "confidence": confidence.score,
                    "context_status": confidence.status,
                    "learning_level": level,
                    "learning_mode": adaptive.mode,
                    "times_seen": progress.seen,
                }
            )

    return {
        "should_teach": result.should_teach,
        "reason": result.reason,
        "items": items,
    }


@app.post("/v1/github-file/learn")
def learn_github_file(
    request: GitHubFileLearnRequest,
) -> dict:
    file = github_file_reader.read_url(
        request.url
    )

    items = context_block_teaching.explain(
        file.content
    )

    return {
        "repository":
            f"{file.owner}/{file.repo}",
        "ref":
            file.ref,
        "path":
            file.path,
        "total_lines":
            len(
                file.content.splitlines()
            ),
        "total_ideas":
            len(items),
        "items": [
            {
                "start_line":
                    item.start_line,
                "end_line":
                    item.end_line,
                "code":
                    item.code,
                "explanation":
                    item.explanation,
                "why":
                    item.why,
                "input_from":
                    item.input_from,
                "output_to":
                    item.output_to,
                "experiment":
                    item.experiment,
                "skill_id":
                    primary_human_skill(
                        item.code
                    ),
                "skill_name":
                    (
                        get_human_skill(
                            primary_human_skill(
                                item.code
                            )
                        ).name
                        if primary_human_skill(
                            item.code
                        )
                        else None
                    ),
                "check":
                    (
                        lambda check: {
                            "question":
                                check.question,
                            "options":
                                list(
                                    check.options
                                ),
                            "explanation":
                                check.explanation,
                        }
                    )(
                        learning_check_engine.build(
                            code=item.code,
                            input_from=item.input_from,
                            output_to=item.output_to,
                        )
                    ),
            }
            for item in items
        ],
    }


@app.post("/v1/learning/check-answer")
def check_learning_answer(
    request: LearningCheckAnswerRequest,
) -> dict:
    check = learning_check_engine.build(
        code=request.code,
        input_from=request.input_from,
        output_to=request.output_to,
    )

    if request.selected_index >= len(
        check.options
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid answer option.",
        )

    correct = (
        request.selected_index
        == check.correct_index
    )

    feedback = (
        adaptive_human_learning
        .record_answer(
            user_id=request.user_id,
            skill_id=request.skill_id,
            correct=correct,
        )
    )

    return {
        "correct":
            correct,
        "explanation":
            check.explanation,
        "mastery_level":
            feedback.mastery_level,
        "message":
            feedback.message,
        "next_step":
            feedback.next_step,
    }


@app.post("/v1/learning/answer")
def record_learning_answer(
    request: HumanLearningAnswerRequest,
) -> dict:
    feedback = (
        adaptive_human_learning
        .record_answer(
            user_id=request.user_id,
            skill_id=request.skill_id,
            correct=request.correct,
        )
    )

    return {
        "skill_id":
            feedback.skill_id,
        "skill_name":
            feedback.skill_name,
        "simple_meaning":
            feedback.simple_meaning,
        "mastery_level":
            feedback.mastery_level,
        "seen":
            feedback.seen,
        "correct":
            feedback.correct,
        "incorrect":
            feedback.incorrect,
        "mastery":
            feedback.mastery,
        "message":
            feedback.message,
        "next_step":
            feedback.next_step,
    }


@app.post("/v1/context-block-learn")
def context_block_learn(
    request: LineByLineRequest,
) -> dict:
    items = context_block_teaching.explain(
        request.code
    )

    response_items = []

    for item in items:
        skill_id = primary_human_skill(
            item.code
        )

        skill = (
            get_human_skill(skill_id)
            if skill_id
            else None
        )

        policy = None

        if (
            request.user_id
            and skill_id
            and skill is not None
        ):
            progress = human_skill_memory.get(
                user_id=request.user_id,
                skill_id=skill_id,
            )

            policy = (
                adaptive_teaching_policy.decide(
                    seen=progress.seen,
                    correct=progress.correct,
                    incorrect=progress.incorrect,
                )
            )

        check = learning_check_engine.build(
            code=item.code,
            input_from=item.input_from,
            output_to=item.output_to,
        )

        response_items.append(
            {
                "start_line":
                    item.start_line,
                "end_line":
                    item.end_line,
                "code":
                    item.code,
                "explanation":
                    item.explanation,
                "why":
                    item.why,
                "input_from":
                    item.input_from,
                "output_to":
                    item.output_to,
                "experiment":
                    item.experiment,
                "skill_id":
                    skill_id,
                "skill_name":
                    (
                        skill.name
                        if skill
                        else None
                    ),
                "teaching_policy":
                    (
                        {
                            "level":
                                policy.level,
                            "explanation_depth":
                                policy.explanation_depth,
                            "show_why":
                                policy.show_why,
                            "show_input_output":
                                policy.show_input_output,
                            "show_experiment":
                                policy.show_experiment,
                            "require_check":
                                policy.require_check,
                            "message":
                                policy.message,
                        }
                        if policy
                        else None
                    ),
                "check":
                    {
                        "question":
                            check.question,
                        "options":
                            list(
                                check.options
                            ),
                    },
            }
        )

    return {
        "total_ideas": len(
            response_items
        ),
        "items": response_items,
    }


@app.post("/v1/context-learn")
def context_learn(
    request: LineByLineRequest,
) -> dict:
    items = context_aware_teaching.explain(
        request.code
    )

    return {
        "items": [
            {
                "line_number":
                    item.line_number,
                "code":
                    item.code,
                "explanation":
                    item.simple_explanation,
                "why":
                    item.why_it_matters,
                "input_from":
                    item.input_from,
                "output_to":
                    item.output_to,
                "consequence":
                    item.consequence,
            }
            for item in items
        ]
    }


@app.post("/v1/line-by-line")
def line_by_line(
    request: LineByLineRequest,
) -> dict:
    items = (
        line_by_line_explainer
        .explain(request.code)
    )

    return {
        "total_lines":
            len(
                request.code.splitlines()
            ),
        "explained_lines":
            len(items),
        "items": [
            {
                "line_number":
                    item.line_number,
                "code":
                    item.code,
                "explanation":
                    item.explanation,
                "why":
                    item.why,
                "challenge":
                    item.challenge,
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
