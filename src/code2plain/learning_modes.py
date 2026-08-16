from __future__ import annotations

from typing import Any

from code2plain.localization import Localizer


class LearningModeBuilder:
    """
    Builds pedagogical modes independently from language.
    """

    def __init__(
        self,
        localizer: Localizer | None = None,
    ) -> None:
        self._localizer = (
            localizer
            or Localizer()
        )

    def apply(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        for section in result.get(
            "sections",
            [],
        ):
            section[
                "learning_modes"
            ] = self._build_modes(
                section
            )

        return result

    def _build_modes(
        self,
        section: dict[str, Any],
    ) -> dict[str, Any]:
        concept = section.get(
            "concept",
            "PROCESS",
        )

        concept_label = (
            section.get(
                "concept_label"
            )
            or self._localizer
            .concept_label(
                concept
            )
        )

        return {
            "learn": {
                "heading":
                    concept_label,

                "primary_label":
                    self._localizer.t(
                        "mode.learn.simple"
                    ),

                "primary":
                    self._beginner(
                        section,
                        "primary",
                    ),

                "secondary_label":
                    self._localizer.t(
                        "mode.learn.key"
                    ),

                "secondary":
                    self._beginner(
                        section,
                        "key",
                    ),
            },

            "understand": {
                "heading":
                    self._localizer.t(
                        "mode.understand."
                        "heading",
                        concept=
                            concept_label,
                    ),

                "primary_label":
                    self._localizer.t(
                        "mode.understand."
                        "simple"
                    ),

                "primary":
                    self._understand(
                        section,
                        "primary",
                    ),

                "secondary_label":
                    self._localizer.t(
                        "mode.understand."
                        "why"
                    ),

                "secondary":
                    self._understand(
                        section,
                        "why",
                    ),
            },

            "deep": {
                "heading":
                    self._localizer.t(
                        "mode.deep.heading",
                        concept=
                            concept_label,
                    ),

                "primary_label":
                    self._localizer.t(
                        "mode.deep.mechanics"
                    ),

                "primary":
                    self._deep(
                        section,
                        "mechanics",
                    ),

                "secondary_label":
                    self._localizer.t(
                        "mode.deep.syntax"
                    ),

                "secondary":
                    self._deep_syntax(
                        section
                    ),

                "technical":
                    self._deep(
                        section,
                        "technical",
                    ),
            },
        }

    def _beginner(
        self,
        section: dict[str, Any],
        kind: str,
    ) -> str:
        concept = section.get(
            "concept",
            "PROCESS",
        )

        key = (
            f"beginner.{concept}.{kind}"
        )

        value = (
            self._localizer
            .t(key)
        )

        if value == key:
            fallback_field = (
                "what_it_does"
                if kind == "primary"
                else "what_to_learn"
            )

            return section.get(
                fallback_field,
                "",
            )

        return value

    def _understand(
        self,
        section: dict[str, Any],
        kind: str,
    ) -> str:
        concept = section.get(
            "concept",
            "PROCESS",
        )

        key = (
            f"understand."
            f"{concept}."
            f"{kind}"
        )

        value = (
            self._localizer
            .t(key)
        )

        if value == key:
            if kind == "why":
                return (
                    self._localizer
                    .t(
                        "understand."
                        "generic.why"
                    )
                )

            return section.get(
                "what_it_does",
                "",
            )

        return value

    def _deep(
        self,
        section: dict[str, Any],
        kind: str,
    ) -> str:
        concept = section.get(
            "concept",
            "PROCESS",
        )

        key = (
            f"deep."
            f"{concept}."
            f"{kind}"
        )

        value = (
            self._localizer
            .t(key)
        )

        if value == key:
            return (
                self._localizer
                .t(
                    f"deep.generic."
                    f"{kind}"
                )
            )

        return value

    def _deep_syntax(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get(
            "concept",
            "PROCESS",
        )

        key = (
            f"deep."
            f"{concept}."
            "syntax"
        )

        value = (
            self._localizer
            .t(key)
        )

        if value != key:
            return value

        code = section.get(
            "code",
            "",
        )

        if "=" in code:
            return (
                self._localizer
                .t(
                    "deep.generic."
                    "assignment"
                )
            )

        return (
            self._localizer
            .t(
                "deep.generic.syntax"
            )
        )
