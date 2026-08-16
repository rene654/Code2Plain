from __future__ import annotations

from dataclasses import asdict
from typing import Any

from code2plain.engine.explanation_engine import (
    ExplanationEngine,
)
from code2plain.learning_modes import (
    LearningModeBuilder,
)
from code2plain.localization import (
    DEFAULT_LANGUAGE,
    Localizer,
)
from code2plain.semantic_enricher import (
    SemanticEnricher,
)


class Code2PlainService:
    """
    Stable application interface for Code2Plain.

    Default language:
        Spanish

    Supported localization can be changed without
    changing the explanation engine.
    """

    def __init__(
        self,
        engine: ExplanationEngine | None = None,
        *,
        language: str = DEFAULT_LANGUAGE,
        localizer: Localizer | None = None,
        enricher: SemanticEnricher | None = None,
        mode_builder: LearningModeBuilder | None = None,
    ) -> None:
        self.language = language

        self._engine = (
            engine
            or ExplanationEngine()
        )

        self._localizer = (
            localizer
            or Localizer(
                language
            )
        )

        self._enricher = (
            enricher
            or SemanticEnricher(
                self._localizer
            )
        )

        self._mode_builder = (
            mode_builder
            or LearningModeBuilder(
                self._localizer
            )
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

        output = (
            self._mode_builder
            .apply(enriched)
        )

        output["language"] = (
            self.language
        )

        return output
