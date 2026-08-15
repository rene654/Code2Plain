from __future__ import annotations

from dataclasses import asdict
from typing import Any

from code2plain.engine.explanation_engine import ExplanationEngine


class Code2PlainService:
    """
    Stable application interface for Code2Plain.

    Consumers:
    - ChatGPT / MCP
    - Ralph OS
    - Browser overlay
    - Desktop UI
    - Future AI providers
    """

    def __init__(
        self,
        engine: ExplanationEngine | None = None,
    ) -> None:
        self._engine = engine or ExplanationEngine()

    def explain_code(
        self,
        code: str,
    ) -> dict[str, Any]:
        result = self._engine.explain_script(code)
        return asdict(result)
