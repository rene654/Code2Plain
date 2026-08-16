from __future__ import annotations

from typing import Any


class LearningModeBuilder:
    """
    Builds multiple pedagogical views of the same code section.

    Modes:
    - Learn: what it does + concept to learn
    - Understand: role inside the overall program flow
    - Deep Dive: mechanics, syntax, and technical detail

    This layer is deterministic and does not require an LLM.
    """

    def apply(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        for section in result.get("sections", []):
            section["learning_modes"] = (
                self._build_modes(section)
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

        return {
            "learn": {
                "heading": concept,
                "primary_label": "IN SIMPLE WORDS",
                "primary": self._beginner_explanation(
                    section
                ),
                "secondary_label": "KEY IDEA",
                "secondary": self._beginner_key_idea(
                    section
                ),
            },
            "understand": {
                "heading": f"{concept} IN THE FLOW",
                "primary_label": "PLAIN ENGLISH",
                "primary": self._understand(
                    section
                ),
                "secondary_label": "WHY IT EXISTS",
                "secondary": self._why_it_exists(
                    section
                ),
            },
            "deep": {
                "heading": f"{concept} · DEEP DIVE",
                "primary_label": "MECHANICS",
                "primary": self._mechanics(
                    section
                ),
                "secondary_label": "SYNTAX FOCUS",
                "secondary": self._syntax_focus(
                    section
                ),
                "technical": self._technical_note(
                    section
                ),
            },
        }

    def _beginner_explanation(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get(
            "concept"
        )

        mapping = {
            "IMPORT": (
                "Python brings in a tool that this program "
                "will need later."
            ),
            "LOAD DATA": (
                "This line opens the data file and puts its "
                "information inside Python so we can work "
                "with it."
            ),
            "FILTER": (
                "This line removes the rows we do not want "
                "and keeps only the ones that match the rule."
            ),
            "AGGREGATE": (
                "This step groups similar rows together and "
                "turns them into a smaller summary."
            ),
            "EXPORT": (
                "This line saves the result into a file that "
                "you can open or share outside Python."
            ),
            "TRANSFORM": (
                "This line changes some information into a "
                "new form that the program can use next."
            ),
            "DECIDE": (
                "This part lets the program choose what to "
                "do depending on whether something is true "
                "or false."
            ),
            "REPEAT": (
                "This part repeats the same action several "
                "times automatically."
            ),
            "DEFINE": (
                "This creates a reusable set of instructions "
                "that can be used again later."
            ),
            "CALL": (
                "This tells Python to run a set of "
                "instructions that already exists."
            ),
        }

        return mapping.get(
            concept,
            section.get(
                "what_it_does",
                "",
            ),
        )

    def _beginner_key_idea(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get(
            "concept"
        )

        mapping = {
            "IMPORT": (
                "Importing means adding a tool to your "
                "program instead of building it yourself."
            ),
            "LOAD DATA": (
                "Before Python can analyze data, that data "
                "has to enter the program."
            ),
            "FILTER": (
                "Filtering means keeping only the data that "
                "follows a rule."
            ),
            "AGGREGATE": (
                "Aggregating means combining many detailed "
                "rows into useful totals or summaries."
            ),
            "EXPORT": (
                "Exporting means taking the result out of "
                "Python and saving it somewhere useful."
            ),
            "TRANSFORM": (
                "Transforming means changing data from one "
                "form into another."
            ),
            "DECIDE": (
                "Conditions let software make different "
                "choices."
            ),
            "REPEAT": (
                "Loops save you from writing the same action "
                "again and again."
            ),
            "DEFINE": (
                "Functions let you reuse instructions."
            ),
            "CALL": (
                "Calling means asking Python to run something "
                "that was already defined."
            ),
        }

        return mapping.get(
            concept,
            section.get(
                "what_to_learn",
                "",
            ),
        )

    def _understand(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get("concept")

        mapping = {
            "IMPORT": (
                "The program prepares the external tools "
                "it needs before doing the actual work."
            ),
            "LOAD DATA": (
                "Information enters the program here and "
                "becomes available for later processing."
            ),
            "FILTER": (
                "The program reduces the current dataset "
                "to only the records relevant to the task."
            ),
            "AGGREGATE": (
                "Detailed records are converted into a "
                "smaller summary that is easier to analyze."
            ),
            "EXPORT": (
                "The program takes its internal result and "
                "writes it somewhere outside Python."
            ),
            "TRANSFORM": (
                "This step changes or prepares information "
                "for another part of the program."
            ),
            "DECIDE": (
                "The program chooses which path to follow "
                "based on a condition."
            ),
            "REPEAT": (
                "The same operation is applied repeatedly "
                "instead of being written many times."
            ),
            "DEFINE": (
                "Reusable behavior is packaged so another "
                "part of the program can call it later."
            ),
            "CALL": (
                "Previously defined behavior is executed "
                "at this point in the program."
            ),
        }

        return mapping.get(
            concept,
            section.get(
                "what_it_does",
                "",
            ),
        )

    def _why_it_exists(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get("concept")

        mapping = {
            "IMPORT": (
                "Without this step, Python would not know "
                "about functionality provided by the library."
            ),
            "LOAD DATA": (
                "A program cannot analyze information until "
                "that information has entered the workflow."
            ),
            "FILTER": (
                "Removing irrelevant records makes later "
                "calculations operate only on the data that "
                "matters."
            ),
            "AGGREGATE": (
                "Raw rows are often too detailed for a "
                "decision. Aggregation turns them into "
                "business-level information."
            ),
            "EXPORT": (
                "A result becomes useful to people and other "
                "systems when it can leave the program."
            ),
            "TRANSFORM": (
                "Intermediate transformations move data "
                "closer to the form required by the final "
                "result."
            ),
            "DECIDE": (
                "Conditions allow software to react "
                "differently to different situations."
            ),
            "REPEAT": (
                "Loops automate repetitive work and reduce "
                "duplicated code."
            ),
            "DEFINE": (
                "Reusable functions make code easier to "
                "maintain, test, and understand."
            ),
            "CALL": (
                "Calls connect reusable behavior with the "
                "moment when that behavior is needed."
            ),
        }

        return mapping.get(
            concept,
            (
                "This step contributes to the program's "
                "input, transformation, decision, or output "
                "flow."
            ),
        )

    def _mechanics(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get("concept")
        code = section.get("code", "")

        if concept == "IMPORT":
            return (
                "Python resolves the requested module and "
                "makes its objects available to this file."
            )

        if concept == "LOAD DATA":
            return (
                "A library function reads an external source "
                "and returns an in-memory data structure, "
                "which is assigned to a variable."
            )

        if concept == "FILTER":
            if "==" in code and "[" in code:
                return (
                    "The comparison creates a Boolean mask: "
                    "each row evaluates to True or False. "
                    "The outer brackets keep the rows whose "
                    "mask value is True."
                )

        if concept == "AGGREGATE":
            return (
                "The data is partitioned into groups. An "
                "aggregation function is then evaluated "
                "independently for each group."
            )

        if concept == "EXPORT":
            return (
                "The current in-memory object is serialized "
                "into an external file format."
            )

        return (
            "Python evaluates this statement according to "
            "its syntax and stores or uses the resulting "
            "value."
        )

    def _syntax_focus(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get("concept")
        code = section.get("code", "")

        if concept == "IMPORT":
            return (
                "`import ... as ...` loads a module and can "
                "assign it a shorter local alias."
            )

        if concept == "LOAD DATA":
            return (
                "The expression on the right side of `=` is "
                "evaluated first; its returned value is then "
                "assigned to the variable on the left."
            )

        if concept == "FILTER":
            return (
                "`df[condition]` is pandas indexing syntax. "
                "The expression inside the brackets decides "
                "which rows are returned."
            )

        if concept == "AGGREGATE":
            return (
                "Method chaining applies operations from "
                "left to right: grouping first, column "
                "selection next, aggregation last."
            )

        if concept == "EXPORT":
            return (
                "Dot notation calls a method belonging to "
                "the current object, such as `.to_excel()`."
            )

        if "=" in code:
            return (
                "`=` is assignment: Python evaluates the "
                "right side and binds that result to the "
                "name on the left."
            )

        return (
            "Read the expression from the innermost "
            "operation outward, following Python's normal "
            "evaluation rules."
        )

    def _technical_note(
        self,
        section: dict[str, Any],
    ) -> str:
        concept = section.get("concept")

        mapping = {
            "IMPORT": (
                "Imports are cached in `sys.modules`, so a "
                "module is normally initialized only once "
                "per Python process."
            ),
            "LOAD DATA": (
                "For large datasets, loading everything into "
                "memory may become expensive. Chunking or "
                "database-side filtering can reduce memory "
                "usage."
            ),
            "FILTER": (
                "In pandas, Boolean masks must align with "
                "the DataFrame index. Missing values and "
                "type mismatches can affect comparisons."
            ),
            "AGGREGATE": (
                "`groupby()` commonly uses a split → apply "
                "→ combine model: split rows into groups, "
                "apply an operation, then combine results."
            ),
            "EXPORT": (
                "Serialization format affects file size, "
                "data types, interoperability, and write "
                "performance."
            ),
        }

        return mapping.get(
            concept,
            (
                "Technical behavior depends on the data "
                "types, library implementation, and runtime "
                "context surrounding this statement."
            ),
        )
