from __future__ import annotations

from dataclasses import asdict
from typing import Any

from code2plain.engine.explanation_engine import ExplanationEngine
from code2plain.learning_modes import LearningModeBuilder
from code2plain.semantic_enricher import SemanticEnricher


class Code2PlainService:
    """
    Stable application interface for Code2Plain.

    Pipeline:

    source code
        ↓
    ExplanationEngine
        ↓
    SemanticEnricher
        ↓
    LearningModeBuilder
        ↓
    consumer
    """

    def __init__(
        self,
        engine: ExplanationEngine | None = None,
        enricher: SemanticEnricher | None = None,
        mode_builder: LearningModeBuilder | None = None,
    ) -> None:
        self._engine = (
            engine
            or ExplanationEngine()
        )

        self._enricher = (
            enricher
            or SemanticEnricher()
        )

        self._mode_builder = (
            mode_builder
            or LearningModeBuilder()
        )

    def explain_code(
        self,
        code: str,
    ) -> dict[str, Any]:
        result = (
            self._engine
            .explain_script(code)
        )

        serialized = asdict(
            result
        )

        enriched = (
            self._enricher
            .enrich(serialized)
        )

        return (
            self._mode_builder
            .apply(enriched)
        )
