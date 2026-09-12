from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ActiveModificationChallenge:
    kind: str
    concept: str
    prompt: str
    expected_value: int
class ActiveModificationEngine:
    _filter_pattern = re.compile(
        r'(?P<target>\w+)\s*=\s*'
        r'(?P<source>\w+)\['
        r'(?P=source)\["(?P<column>[^"]+)"\]\s*'
        r'(?P<operator>>)\s*'
        r'(?P<value>\d+)'
        r'\]'
    )
    def build(
        self,
        *,
        code: str,
    ) -> ActiveModificationChallenge | None:
        match = self._filter_pattern.fullmatch(
            code.strip()
        )
        if match is None:
            return None
        current_value = int(
            match.group("value")
        )
        expected_value = (
            current_value + 500
        )
        column = match.group("column")
        return ActiveModificationChallenge(
            kind="modify_filter",
            concept="FILTER",
            prompt=(
                "Modifica esta línea para conservar "
                f"solo las filas donde {column} sea "
                f"mayor a {expected_value}."
            ),
            expected_value=expected_value,
        )
    def verify(
        self,
        *,
        original_code: str,
        answer: str,
    ) -> bool:
        challenge = self.build(
            code=original_code,
        )
        if challenge is None:
            return False
        original = self._filter_pattern.fullmatch(
            original_code.strip()
        )
        candidate = self._filter_pattern.fullmatch(
            answer.strip()
        )
        if (
            original is None
            or candidate is None
        ):
            return False
        return (
            candidate.group("target")
            == original.group("target")
            and candidate.group("source")
            == original.group("source")
            and candidate.group("column")
            == original.group("column")
            and candidate.group("operator")
            == original.group("operator")
            and int(candidate.group("value"))
            == challenge.expected_value
        )
active_modification_engine = ActiveModificationEngine()
