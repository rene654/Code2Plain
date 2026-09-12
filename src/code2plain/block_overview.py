from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class BlockOverviewStep:
    title: str
    detail: str
@dataclass(frozen=True)
class BlockOverview:
    title: str
    summary: str
    steps: tuple[BlockOverviewStep, ...]
class BlockOverviewEngine:
    def build(
        self,
        *,
        code: str,
    ) -> BlockOverview | None:
        steps: list[BlockOverviewStep] = []
        if "read_csv(" in code:
            steps.append(
                BlockOverviewStep(
                    title="Cargar datos",
                    detail=(
                        "Abre un archivo CSV y lo convierte "
                        "en datos que pandas puede trabajar."
                    ),
                )
            )
        if re.search(
            r'\w+\[\w+\["[^"]+"\]\s*(?:>=|<=|==|!=|>|<)',
            code,
        ):
            steps.append(
                BlockOverviewStep(
                    title="Filtrar datos",
                    detail=(
                        "Conserva únicamente las filas "
                        "que cumplen una condición."
                    ),
                )
            )
        if (
            ".groupby(" in code
            and ".sum()" in code
        ):
            steps.append(
                BlockOverviewStep(
                    title="Agrupar y sumar",
                    detail=(
                        "Forma grupos, selecciona los valores "
                        "relevantes y calcula su suma."
                    ),
                )
            )
        if "print(" in code:
            steps.append(
                BlockOverviewStep(
                    title="Mostrar resultado",
                    detail=(
                        "Envía el resultado final a pantalla."
                    ),
                )
            )
        if not steps:
            return None
        flow = " → ".join(
            step.title
            for step in steps
        )
        return BlockOverview(
            title="Qué hace este bloque",
            summary=flow,
            steps=tuple(steps),
        )
block_overview_engine = BlockOverviewEngine()
