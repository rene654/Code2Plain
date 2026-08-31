from __future__ import annotations

import ast


class HumanSkillDetector:
    """
    Maps code structures to human learning skills.

    It stores skill identifiers only.
    Source code is used transiently for detection.
    """

    def detect(
        self,
        code: str,
    ) -> list[str]:
        source = code.strip()

        if not source:
            return []

        skills: list[str] = []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        for node in ast.walk(tree):
            if isinstance(
                node,
                (ast.Import, ast.ImportFrom),
            ):
                self._add(
                    skills,
                    "IMPORT_USE",
                )

            if isinstance(
                node,
                ast.Assign,
            ):
                self._add(
                    skills,
                    "VARIABLE_USE",
                )

                self._add(
                    skills,
                    "INPUT_OUTPUT",
                )

            if isinstance(
                node,
                ast.Call,
            ):
                if isinstance(
                    node.func,
                    ast.Attribute,
                ):
                    self._add(
                        skills,
                        "METHOD_CALL",
                    )
                else:
                    self._add(
                        skills,
                        "FUNCTION_CALL",
                    )

                self._add(
                    skills,
                    "INPUT_OUTPUT",
                )

            if isinstance(
                node,
                ast.Compare,
            ):
                self._add(
                    skills,
                    "CONTROL_FLOW",
                )

            if isinstance(
                node,
                ast.Subscript,
            ) and self._contains_compare(
                node
            ):
                self._add(
                    skills,
                    "DATA_FILTERING",
                )

            if (
                isinstance(
                    node,
                    ast.Call,
                )
                and isinstance(
                    node.func,
                    ast.Attribute,
                )
            ):
                name = node.func.attr

                if name == "groupby":
                    self._add(
                        skills,
                        "DATA_GROUPING",
                    )

                if name in {
                    "sum",
                    "mean",
                    "min",
                    "max",
                    "count",
                }:
                    self._add(
                        skills,
                        "DATA_SUMMARY",
                    )

        return skills

    def _contains_compare(
        self,
        node: ast.AST,
    ) -> bool:
        return any(
            isinstance(
                child,
                ast.Compare,
            )
            for child in ast.walk(
                node
            )
        )

    def _add(
        self,
        skills: list[str],
        skill_id: str,
    ) -> None:
        if skill_id not in skills:
            skills.append(
                skill_id
            )


human_skill_detector = (
    HumanSkillDetector()
)


SKILL_PRIORITY = (
    "DATA_FILTERING",
    "DATA_GROUPING",
    "DATA_SUMMARY",
    "METHOD_CALL",
    "FUNCTION_CALL",
    "CONTROL_FLOW",
    "INPUT_OUTPUT",
    "VARIABLE_USE",
    "IMPORT_USE",
)


def primary_human_skill(
    code: str,
) -> str | None:
    skills = human_skill_detector.detect(
        code
    )

    for skill_id in SKILL_PRIORITY:
        if skill_id in skills:
            return skill_id

    return (
        skills[0]
        if skills
        else None
    )
