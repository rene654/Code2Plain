from __future__ import annotations

from typing import Any


class SemanticEnricher:
    """
    Adds higher-level programming concepts and more specific
    educational explanations without coupling them to the UI.

    The ExplanationEngine remains responsible for structure.
    This layer improves meaning and learning value.
    """

    def enrich(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        for section in result.get("sections", []):
            self._enrich_section(section)

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

        if section.get("category") == "import":
            self._set(
                section,
                concept="IMPORT",
                title="Import tools",
                what_it_does=(
                    "Loads external tools that the program "
                    "will use later."
                ),
                what_to_learn=(
                    "Imports let Python reuse functionality "
                    "from libraries instead of building "
                    "everything from scratch."
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
                section,
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
            "error_handling": "HANDLE ERROR",
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
        source = "data source"

        if "read_excel(" in normalized:
            source = "Excel file"
        elif "read_csv(" in normalized:
            source = "CSV file"
        elif "read_sql(" in normalized:
            source = "SQL source"
        elif "read_json(" in normalized:
            source = "JSON file"
        elif "read_parquet(" in normalized:
            source = "Parquet file"

        self._set(
            section,
            concept="LOAD DATA",
            title="Load data",
            what_it_does=(
                f"Reads data from an {source} and stores "
                "the result so the program can work with it."
            ),
            what_to_learn=(
                "Loading data is usually the input stage of "
                "a data workflow: information enters the "
                "program before it can be filtered, changed, "
                "or analyzed."
            ),
        )

    def _enrich_filter(
        self,
        section: dict[str, Any],
    ) -> None:
        code = section.get(
            "code",
            "",
        )

        explanation = (
            "Keeps only the rows that satisfy the condition "
            "inside the brackets."
        )

        if '"status"' in code and '"Late"' in code:
            explanation = (
                'Keeps only rows where the "status" column '
                'equals "Late".'
            )

        self._set(
            section,
            concept="FILTER",
            title="Filter records",
            what_it_does=explanation,
            what_to_learn=(
                "Boolean filtering creates a True/False rule "
                "for every row and keeps only the rows where "
                "the rule is True."
            ),
        )

    def _enrich_aggregation(
        self,
        section: dict[str, Any],
        normalized: str,
    ) -> None:
        operation = "aggregate"

        if ".sum(" in normalized:
            operation = "sum"
        elif ".mean(" in normalized:
            operation = "average"
        elif ".count(" in normalized:
            operation = "count"
        elif ".min(" in normalized:
            operation = "minimum"
        elif ".max(" in normalized:
            operation = "maximum"

        explanation = (
            f"Groups related records and calculates a "
            f"{operation} for each group."
        )

        code = section.get(
            "code",
            "",
        )

        if (
            '"supplier"' in code
            and '"amount"' in code
            and operation == "sum"
        ):
            explanation = (
                'Groups the records by "supplier" and sums '
                'the "amount" values to calculate a total '
                "for each supplier."
            )

        self._set(
            section,
            concept="AGGREGATE",
            title="Group and summarize",
            what_it_does=explanation,
            what_to_learn=(
                "Grouping organizes rows by a shared value. "
                "An aggregation such as sum, average, or count "
                "then produces one result for each group."
            ),
        )

    def _enrich_export(
        self,
        section: dict[str, Any],
        normalized: str,
    ) -> None:
        destination = "output file"

        if "to_excel(" in normalized:
            destination = "Excel file"
        elif "to_csv(" in normalized:
            destination = "CSV file"
        elif "to_json(" in normalized:
            destination = "JSON file"
        elif "to_parquet(" in normalized:
            destination = "Parquet file"

        self._set(
            section,
            concept="EXPORT",
            title="Export result",
            what_it_does=(
                f"Writes the processed result to an "
                f"{destination} so it can be used outside "
                "the Python program."
            ),
            what_to_learn=(
                "Exporting is an output stage: the program "
                "turns its internal result into something "
                "another person or system can consume."
            ),
        )

    @staticmethod
    def _set(
        section: dict[str, Any],
        *,
        concept: str,
        title: str,
        what_it_does: str,
        what_to_learn: str,
    ) -> None:
        section["concept"] = concept
        section["title"] = title
        section["what_it_does"] = what_it_does
        section["what_to_learn"] = what_to_learn
