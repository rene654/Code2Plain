from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LineBreakdownPart:
    code: str
    meaning: str
@dataclass(frozen=True)
class LineBreakdown:
    title: str
    summary: str
    parts: tuple[LineBreakdownPart, ...]
class LineBreakdownEngine:
    def build(
        self,
        *,
        code: str,
    ) -> LineBreakdown | None:
        source = code.strip()
        filter_match = re.fullmatch(
            r'(?P<target>\w+)\s*=\s*'
            r'(?P<source>\w+)\['
            r'(?P=source)\["(?P<column>[^"]+)"\]\s*'
            r'(?P<operator>>=|<=|==|!=|>|<)\s*'
            r'(?P<value>[^\]]+)'
            r'\]',
            source,
        )
        if filter_match:
            target = filter_match.group("target")
            data = filter_match.group("source")
            column = filter_match.group("column")
            operator = filter_match.group("operator")
            value = filter_match.group("value").strip()
            return LineBreakdown(
                title="Filtro de datos",
                summary=(
                    f"Toma {data}, conserva las filas donde "
                    f"{column} {operator} {value} y guarda "
                    f"el resultado en {target}."
                ),
                parts=(
                    LineBreakdownPart(
                        code=f"{target} =",
                        meaning=(
                            "Guarda el resultado con este nombre."
                        ),
                    ),
                    LineBreakdownPart(
                        code=f'{data}["{column}"]',
                        meaning=(
                            f"Lee la columna {column} de {data}."
                        ),
                    ),
                    LineBreakdownPart(
                        code=f"{operator} {value}",
                        meaning=(
                            "Construye la condición que cada fila "
                            "debe cumplir."
                        ),
                    ),
                    LineBreakdownPart(
                        code=f"{data}[condición]",
                        meaning=(
                            "Conserva solamente las filas que "
                            "cumplen esa condición."
                        ),
                    ),
                ),
            )
        group_match = re.fullmatch(
            r'(?P<target>\w+)\s*=\s*'
            r'(?P<source>\w+)'
            r'\.groupby\("(?P<group>[^"]+)"\)'
            r'\["(?P<column>[^"]+)"\]'
            r'\.sum\(\)',
            source,
        )
        if group_match:
            target = group_match.group("target")
            data = group_match.group("source")
            group = group_match.group("group")
            column = group_match.group("column")
            return LineBreakdown(
                title="Agrupar y sumar",
                summary=(
                    f"Agrupa {data} por {group}, toma {column}, "
                    f"suma sus valores y guarda el resultado "
                    f"en {target}."
                ),
                parts=(
                    LineBreakdownPart(
                        code=f"{target} =",
                        meaning=(
                            "Guarda el resultado final con este nombre."
                        ),
                    ),
                    LineBreakdownPart(
                        code=data,
                        meaning=(
                            "Es el conjunto de datos que entra "
                            "a esta operación."
                        ),
                    ),
                    LineBreakdownPart(
                        code=f'.groupby("{group}")',
                        meaning=(
                            f"Forma un grupo distinto por cada {group}."
                        ),
                    ),
                    LineBreakdownPart(
                        code=f'["{column}"]',
                        meaning=(
                            f"Elige la columna {column} dentro "
                            "de cada grupo."
                        ),
                    ),
                    LineBreakdownPart(
                        code=".sum()",
                        meaning=(
                            "Suma los valores seleccionados "
                            "dentro de cada grupo."
                        ),
                    ),
                ),
            )
        return None
line_breakdown_engine = LineBreakdownEngine()
