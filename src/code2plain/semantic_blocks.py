from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticBlock:
    start_line: int
    end_line: int
    code: str
    target: str | None
    expression: str
    kind: str


class SemanticBlockExtractor:
    """
    Convert Python source into meaningful executable blocks.

    A multiline assignment such as:

        result = (
            active
            .groupby("customer")
            ["amount"]
            .sum()
        )

    is treated as ONE learning unit.
    """

    def extract(
        self,
        code: str,
    ) -> list[SemanticBlock]:
        tree = ast.parse(code)

        blocks: list[SemanticBlock] = []

        for node in tree.body:
            source = ast.get_source_segment(
                code,
                node,
            )

            if not source:
                continue

            target = None
            expression = source
            kind = type(node).__name__

            if isinstance(node, ast.Assign):
                if (
                    len(node.targets) == 1
                    and isinstance(
                        node.targets[0],
                        ast.Name,
                    )
                ):
                    target = (
                        node.targets[0].id
                    )

                expression = ast.unparse(
                    node.value
                )

                kind = "assignment"

            elif isinstance(node, ast.Import):
                kind = "import"

            elif isinstance(
                node,
                ast.ImportFrom,
            ):
                kind = "import"

            elif isinstance(node, ast.Expr):
                try:
                    expression = ast.unparse(
                        node.value
                    )
                except Exception:
                    expression = source

                kind = "expression"

            blocks.append(
                SemanticBlock(
                    start_line=node.lineno,
                    end_line=getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                    code=source,
                    target=target,
                    expression=expression,
                    kind=kind,
                )
            )

        return blocks


semantic_block_extractor = (
    SemanticBlockExtractor()
)
