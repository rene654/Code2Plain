from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from code2plain.learning.adaptive_digest import (
    AdaptiveSessionDigestBuilder,
)
from code2plain.learning.digest import (
    SessionDigest,
)
from code2plain.learning.profile_store import (
    LearningProfileStore,
)
from code2plain.learning.session_end import (
    AutomaticSessionEndDetector,
    SessionEndDecision,
)
from code2plain.learning.tracker import (
    SessionLearningTracker,
)


@dataclass(frozen=True)
class AutomaticSessionResult:
    decision: SessionEndDecision
    digest: SessionDigest | None


class LearningSessionCoordinator:
    """
    Coordinates automatic session closure.

    When inactivity closes a session:

    1. close session
    2. persist learning profile
    3. build digest

    No user prompt is required.
    """

    def __init__(
        self,
        tracker: SessionLearningTracker,
        profile_store: LearningProfileStore,
        *,
        language: str = "es",
        detector: AutomaticSessionEndDetector | None = None,
    ) -> None:

        self.tracker = tracker
        self.profile_store = profile_store

        self.detector = (
            detector
            or AutomaticSessionEndDetector()
        )

        self.digest_builder = (
            AdaptiveSessionDigestBuilder(
                language
            )
        )

        self._digest: SessionDigest | None = None


    def check(
        self,
        *,
        now: datetime | None = None,
    ) -> AutomaticSessionResult:

        decision = (
            self.detector.auto_close(
                self.tracker.session,
                now=now,
            )
        )

        if (
            decision.state == "CLOSED"
            and self._digest is None
        ):
            self.profile_store.save(
                self.tracker.profile
            )

            self._digest = (
                self.digest_builder.build(
                    self.tracker.session,
                    self.tracker.profile,
                )
            )

        return AutomaticSessionResult(
            decision=decision,
            digest=self._digest,
        )


    @property
    def digest(
        self,
    ) -> SessionDigest | None:

        return self._digest
