import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class DeltaResult:
    is_new: bool
    fingerprint: str


class CodeDeltaTracker:
    """
    Tracks previously seen AI code so Code2Plain
    does not explain the same generated block repeatedly.
    """

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def check(
        self,
        code: str,
    ) -> DeltaResult:
        normalized = code.strip()

        fingerprint = hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

        is_new = fingerprint not in self._seen

        if is_new:
            self._seen.add(fingerprint)

        return DeltaResult(
            is_new=is_new,
            fingerprint=fingerprint,
        )
