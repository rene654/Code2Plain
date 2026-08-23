import re

from code2plain.detection.models import (
    ContentCandidate,
    DetectionResult,
)


class AICodeDetector:
    """
    Decide whether newly observed content should trigger
    automatic Code2Plain learning.

    False positives are intentionally more expensive
    than false negatives.
    """

    AI_SOURCES = {
        "chatgpt",
        "github_copilot",
        "claude",
        "cursor",
    }

    AI_ROLES = {
        "assistant",
        "ai",
    }

    def detect(
        self,
        candidate: ContentCandidate,
    ) -> DetectionResult:
        source = candidate.source.strip().lower()
        role = candidate.author_role.strip().lower()

        if source not in self.AI_SOURCES:
            return DetectionResult(
                should_explain=False,
                confidence=0.05,
                reason="untrusted_source",
            )

        if role not in self.AI_ROLES:
            return DetectionResult(
                should_explain=False,
                confidence=0.10,
                reason="not_ai_authored",
            )

        code = self._extract_code(
            candidate.text,
            candidate.content_type,
        )

        if not code.strip():
            return DetectionResult(
                should_explain=False,
                confidence=0.20,
                reason="no_code_detected",
            )

        if not self._looks_like_code(code):
            return DetectionResult(
                should_explain=False,
                confidence=0.45,
                reason="low_code_confidence",
            )

        return DetectionResult(
            should_explain=True,
            confidence=0.95,
            reason="ai_generated_code",
            code=code.strip(),
        )

    @staticmethod
    def _extract_code(
        text: str,
        content_type: str,
    ) -> str:
        if content_type == "code":
            return text

        fenced = re.search(
            r"```(?:[A-Za-z0-9_+\-#.]+)?\s*\n"
            r"(.*?)"
            r"\n```",
            text,
            flags=re.DOTALL,
        )

        if fenced:
            return fenced.group(1)

        return ""

    @staticmethod
    def _looks_like_code(
        code: str,
    ) -> bool:
        signals = (
            "=",
            "(",
            ")",
            "[",
            "]",
            "def ",
            "class ",
            "import ",
            "return ",
            "if ",
            "for ",
        )

        score = sum(
            signal in code
            for signal in signals
        )

        return score >= 2
