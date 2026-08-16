from __future__ import annotations

from collections import defaultdict

from code2plain.entitlements.models import (
    EntitlementDecision,
    SubscriptionPlan,
)


FEATURE_MOBILE_DIGEST = "mobile_digest"
FEATURE_ADAPTIVE_DIGEST = "adaptive_digest"
FEATURE_MULTI_DEVICE = "multi_device"


class EntitlementService:
    """
    Server-side feature access policy.

    Important separation:

    - QR/device pairing identifies an authorized device.
    - Account plan determines product access.
    - Pairing never grants Premium capabilities.

    This first implementation is deterministic and local.
    A billing provider can replace plan assignment later
    without changing feature consumers.
    """

    def __init__(
        self,
        *,
        free_mobile_digest_limit: int = 3,
    ) -> None:

        if free_mobile_digest_limit < 0:
            raise ValueError(
                "free_mobile_digest_limit cannot be negative"
            )

        self.free_mobile_digest_limit = (
            free_mobile_digest_limit
        )

        self._plans: dict[
            str,
            SubscriptionPlan,
        ] = {}

        self._usage: dict[
            tuple[str, str],
            int,
        ] = defaultdict(int)


    def set_plan(
        self,
        account_id: str,
        plan: SubscriptionPlan | str,
    ) -> None:

        account_id = (
            self._normalize_account_id(
                account_id
            )
        )

        self._plans[
            account_id
        ] = SubscriptionPlan(
            plan
        )


    def get_plan(
        self,
        account_id: str,
    ) -> SubscriptionPlan:

        account_id = (
            self._normalize_account_id(
                account_id
            )
        )

        return self._plans.get(
            account_id,
            SubscriptionPlan.FREE,
        )


    def check(
        self,
        account_id: str,
        feature: str,
    ) -> EntitlementDecision:

        account_id = (
            self._normalize_account_id(
                account_id
            )
        )

        feature = feature.strip()

        if not feature:
            raise ValueError(
                "feature cannot be empty"
            )

        plan = self.get_plan(
            account_id
        )

        if plan is SubscriptionPlan.PRO:
            return EntitlementDecision(
                account_id=account_id,
                feature=feature,
                plan=plan,
                allowed=True,
                reason="Feature included in Pro.",
                usage_limit=None,
                usage_remaining=None,
            )

        if feature == FEATURE_MOBILE_DIGEST:

            used = self._usage[
                (
                    account_id,
                    feature,
                )
            ]

            remaining = max(
                0,
                self.free_mobile_digest_limit
                - used,
            )

            allowed = (
                remaining > 0
            )

            return EntitlementDecision(
                account_id=account_id,
                feature=feature,
                plan=plan,
                allowed=allowed,
                reason=(
                    "Free mobile digest available."
                    if allowed
                    else
                    "Free mobile digest limit reached."
                ),
                usage_limit=(
                    self.free_mobile_digest_limit
                ),
                usage_remaining=remaining,
            )

        if feature == FEATURE_ADAPTIVE_DIGEST:
            return EntitlementDecision(
                account_id=account_id,
                feature=feature,
                plan=plan,
                allowed=True,
                reason=(
                    "Basic adaptive learning is available "
                    "on Free."
                ),
            )

        if feature == FEATURE_MULTI_DEVICE:
            return EntitlementDecision(
                account_id=account_id,
                feature=feature,
                plan=plan,
                allowed=False,
                reason=(
                    "Multiple devices require Pro."
                ),
            )

        return EntitlementDecision(
            account_id=account_id,
            feature=feature,
            plan=plan,
            allowed=False,
            reason=(
                "Feature is not included in Free."
            ),
        )


    def consume(
        self,
        account_id: str,
        feature: str,
    ) -> EntitlementDecision:

        decision = self.check(
            account_id,
            feature,
        )

        if not decision.allowed:
            return decision

        if (
            decision.plan
            is SubscriptionPlan.FREE
            and feature
            == FEATURE_MOBILE_DIGEST
        ):
            key = (
                decision.account_id,
                feature,
            )

            self._usage[
                key
            ] += 1

        return self.check(
            decision.account_id,
            feature,
        )


    def usage_count(
        self,
        account_id: str,
        feature: str,
    ) -> int:

        account_id = (
            self._normalize_account_id(
                account_id
            )
        )

        return self._usage[
            (
                account_id,
                feature,
            )
        ]


    def reset_usage(
        self,
        account_id: str,
        feature: str,
    ) -> None:

        account_id = (
            self._normalize_account_id(
                account_id
            )
        )

        self._usage[
            (
                account_id,
                feature,
            )
        ] = 0


    @staticmethod
    def _normalize_account_id(
        account_id: str,
    ) -> str:

        normalized = (
            account_id.strip()
        )

        if not normalized:
            raise ValueError(
                "account_id cannot be empty"
            )

        return normalized
