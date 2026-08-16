from __future__ import annotations

from typing import Any

from code2plain.localization import Localizer


class SemanticEnricher:
    """
    Detects semantic programming concepts.

    Concept IDs remain language-neutral.
    Visible text is delegated to Localizer.
    """

    def __init__(
        self,
        localizer: Localizer | None = None,
    ) -> None:
        self._localizer = (
            localizer
            or Localizer()
        )

    def enrich(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        for section in result.get(
            "sections",
            [],
        ):
            self._enrich_section(
                section
            )

            concept = section.get(
                "concept",
                "PROCESS",
            )

            section[
                "concept_label"
            ] = (
                self._localizer
                .concept_label(
                    concept
                )
            )

        return result

    def _enrich_section(
        self,
        section: dict[str, Any],
    ) -> None:
        code = section.get(
            "code",
            "",
        )

        normalized = code.lower()

        if (
            section.get("category")
            == "import"
        ):
            self._set(
                section,
                concept="IMPORT",
                title_key="title.import",
                does_key=(
                    "semantic.import.does"
                ),
                learn_key=(
                    "semantic.import.learn"
                ),
            )
            return

        if any(
            token in normalized
            for token in (
                "read_excel(",
                "read_csv(",
                "read_sql(",
                "read_json(",
                "read_parquet(",
            )
        ):
            self._enrich_data_load(
                section,
                normalized,
            )
            return

        if (
            "groupby(" in normalized
            and any(
                aggregate in normalized
                for aggregate in (
                    ".sum(",
                    ".mean(",
                    ".count(",
                    ".min(",
                    ".max(",
                )
            )
        ):
            self._enrich_aggregation(
                section,
                normalized,
            )
            return

        if (
            "[" in code
            and "==" in code
            and section.get("category")
            == "assignment"
        ):
            self._enrich_filter(
                section
            )
            return

        if any(
            token in normalized
            for token in (
                "to_excel(",
                "to_csv(",
                "to_json(",
                "to_parquet(",
            )
        ):
            self._enrich_export(
                section,
                normalized,
            )
            return

        category = section.get(
            "category",
            "unknown",
        )

        concept_map = {
            "assignment": "TRANSFORM",
            "condition": "DECIDE",
            "loop": "REPEAT",
            "function": "DEFINE",
            "function_call": "CALL",
            "return": "RETURN",
            "error_handling":
                "HANDLE ERROR",
            "class": "MODEL",
        }

        section["concept"] = (
            concept_map.get(
                category,
                "PROCESS",
            )
        )

    def _enrich_data_load(
        self,
        section: dict[str, Any],
        normalized: str,
    ) -> None:
        source_key = (
            "source.generic"
        )

        if "read_excel(" in normalized:
            source_key = (
                "source.excel"
            )
        elif "read_csv(" in normalized:
            source_key = (
                "source.csv"
            )
        elif "read_sql(" in normalized:
            source_key = (
                "source.sql"
            )
        elif "read_json(" in normalized:
            source_key = (
                "source.json"
            )
        elif "read_parquet(" in normalized:
            source_key = (
                "source.parquet"
            )

        source = (
            self._localizer
            .t(source_key)
        )

        self._set(
            section,
            concept="LOAD DATA",
            title_key="title.load",
            does_key=(
                "semantic.load.does"
            ),
            learn_key=(
                "semantic.load.learn"
            ),
            does_values={
                "source": source,
            },
        )

    def _enrich_filter(
        self,
        section: dict[str, Any],
    ) -> None:
        code = section.get(
            "code",
            "",
        )

        does_key = (
            "semantic.filter.does"
        )

        if (
            '"status"' in code
            and '"Late"' in code
        ):
            does_key = (
                "semantic.filter."
                "status_late"
            )

        self._set(
            section,
            concept="FILTER",
            title_key="title.filter",
            does_key=does_key,
            learn_key=(
                "semantic.filter.learn"
            ),
        )

    def _enrich_aggregation(
        self,
        section: dict[str, Any],
        normalized: str,
    ) -> None:
        operation_key = (
            "operation.generic"
        )

        if ".sum(" in normalized:
            operation_key = (
                "operation.sum"
            )
        elif ".mean(" in normalized:
            operation_key = (
                "operation.mean"
            )
        elif ".count(" in normalized:
            operation_key = (
                "operation.count"
            )
        elif ".min(" in normalized:
            operation_key = (
                "operation.min"
            )
        elif ".max(" in normalized:
            operation_key = (
                "operation.max"
            )

        operation = (
            self._localizer
            .t(operation_key)
        )

        does_key = (
            "semantic.aggregate.does"
        )

        does_values = {
            "operation": operation,
        }

        code = section.get(
            "code",
            "",
        )

        if (
            '"supplier"' in code
            and '"amount"' in code
            and ".sum(" in normalized
        ):
            does_key = (
                "semantic.aggregate."
                "supplier_amount"
            )

            does_values = {}

        self._set(
            section,
            concept="AGGREGATE",
            title_key="title.aggregate",
            does_key=does_key,
            learn_key=(
                "semantic.aggregate.learn"
            ),
            does_values=does_values,
        )

    def _enrich_export(
        self,
        section: dict[str, Any],
        normalized: str,
    ) -> None:
        destination_key = (
            "destination.generic"
        )

        if "to_excel(" in normalized:
            destination_key = (
                "destination.excel"
            )
        elif "to_csv(" in normalized:
            destination_key = (
                "destination.csv"
            )
        elif "to_json(" in normalized:
            destination_key = (
                "destination.json"
            )
        elif "to_parquet(" in normalized:
            destination_key = (
                "destination.parquet"
            )

        destination = (
            self._localizer
            .t(destination_key)
        )

        self._set(
            section,
            concept="EXPORT",
            title_key="title.export",
            does_key=(
                "semantic.export.does"
            ),
            learn_key=(
                "semantic.export.learn"
            ),
            does_values={
                "destination":
                    destination,
            },
        )

    def _set(
        self,
        section: dict[str, Any],
        *,
        concept: str,
        title_key: str,
        does_key: str,
        learn_key: str,
        does_values: (
            dict[str, Any]
            | None
        ) = None,
    ) -> None:
        section["concept"] = concept

        section["title"] = (
            self._localizer
            .t(title_key)
        )

        section["what_it_does"] = (
            self._localizer
            .t(
                does_key,
                **(
                    does_values
                    or {}
                ),
            )
        )

        section["what_to_learn"] = (
            self._localizer
            .t(learn_key)
        )
