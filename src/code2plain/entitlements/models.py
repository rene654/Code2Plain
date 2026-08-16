from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SubscriptionPlan(str, Enum):
    FREE = "free"
    PRO = "pro"


@dataclass(frozen=True)
class EntitlementDecision:
    account_id: str
    feature: str
    plan: SubscriptionPlan
    allowed: bool
    reason: str
    usage_limit: int | None = None
    usage_remaining: int | None = None
