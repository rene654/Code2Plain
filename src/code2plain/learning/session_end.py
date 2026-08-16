from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)

from code2plain.learning.models import (
    LearningSession,
    utc_now,
)


@dataclass(frozen=True)
class SessionEndDecision:
    state: str
    should_close: bool
    idle_seconds: int
    reason: str


class AutomaticSessionEndDetector:
    """
    Deterministic inactivity-based session lifecycle.

    States:

    ACTIVE
    IDLE
    READY_TO_CLOSE
    CLOSED

    Automation rule:
    a learning session should close automatically after
    sufficient inactivity without requiring a user action.
    """

    def __init__(
        self,
        *,
        idle_after_minutes: int = 20,
        grace_minutes: int = 5,
    ) -> None:

        if idle_after_minutes <= 0:
            raise ValueError(
                "idle_after_minutes must be positive"
            )

        if grace_minutes < 0:
            raise ValueError(
                "grace_minutes cannot be negative"
            )

        self.idle_after = timedelta(
            minutes=idle_after_minutes
        )

        self.grace_period = timedelta(
            minutes=grace_minutes
        )


    @property
    def close_after(
        self,
    ) -> timedelta:

        return (
            self.idle_after
            + self.grace_period
        )


    def evaluate(
        self,
        session: LearningSession,
        *,
        now: datetime | None = None,
    ) -> SessionEndDecision:

        if session.is_closed:
            return SessionEndDecision(
                state="CLOSED",
                should_close=False,
                idle_seconds=0,
                reason=(
                    "Session is already closed."
                ),
            )

        timestamp = (
            now
            or utc_now()
        )

        idle_time = (
            timestamp
            - session.last_activity_at
        )

        idle_seconds = max(
            0,
            int(
                idle_time.total_seconds()
            ),
        )

        if idle_time < self.idle_after:
            return SessionEndDecision(
                state="ACTIVE",
                should_close=False,
                idle_seconds=idle_seconds,
                reason=(
                    "Recent activity detected."
                ),
            )

        if idle_time < self.close_after:
            return SessionEndDecision(
                state="IDLE",
                should_close=False,
                idle_seconds=idle_seconds,
                reason=(
                    "Session is inactive but still "
                    "inside the grace period."
                ),
            )

        return SessionEndDecision(
            state="READY_TO_CLOSE",
            should_close=True,
            idle_seconds=idle_seconds,
            reason=(
                "Inactivity threshold and grace "
                "period have both elapsed."
            ),
        )


    def auto_close(
        self,
        session: LearningSession,
        *,
        now: datetime | None = None,
    ) -> SessionEndDecision:

        timestamp = (
            now
            or utc_now()
        )

        decision = self.evaluate(
            session,
            now=timestamp,
        )

        if decision.should_close:
            session.ended_at = timestamp

            return SessionEndDecision(
                state="CLOSED",
                should_close=True,
                idle_seconds=(
                    decision.idle_seconds
                ),
                reason=(
                    "Session closed automatically "
                    "after inactivity."
                ),
            )

        return decision
