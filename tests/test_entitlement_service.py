from code2plain.entitlements import (
    EntitlementService,
    SubscriptionPlan,
)
from code2plain.entitlements.service import (
    FEATURE_ADAPTIVE_DIGEST,
    FEATURE_MOBILE_DIGEST,
    FEATURE_MULTI_DEVICE,
)


def test_unknown_account_defaults_to_free():
    service = EntitlementService()

    assert (
        service.get_plan(
            "account_1"
        )
        == SubscriptionPlan.FREE
    )


def test_pro_has_mobile_digest_access():
    service = EntitlementService()

    service.set_plan(
        "account_1",
        SubscriptionPlan.PRO,
    )

    decision = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert decision.allowed
    assert (
        decision.plan
        == SubscriptionPlan.PRO
    )

    assert decision.usage_limit is None


def test_free_mobile_digest_has_usage_limit():
    service = EntitlementService(
        free_mobile_digest_limit=3
    )

    decision = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert decision.allowed
    assert decision.usage_limit == 3
    assert decision.usage_remaining == 3


def test_free_usage_is_consumed():
    service = EntitlementService(
        free_mobile_digest_limit=2
    )

    service.consume(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    decision = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert decision.allowed
    assert decision.usage_remaining == 1


def test_free_limit_eventually_blocks():
    service = EntitlementService(
        free_mobile_digest_limit=2
    )

    service.consume(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    service.consume(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    decision = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert not decision.allowed
    assert decision.usage_remaining == 0


def test_pro_usage_does_not_decrement():
    service = EntitlementService(
        free_mobile_digest_limit=1
    )

    service.set_plan(
        "account_1",
        "pro",
    )

    for _ in range(10):
        service.consume(
            "account_1",
            FEATURE_MOBILE_DIGEST,
        )

    assert (
        service.usage_count(
            "account_1",
            FEATURE_MOBILE_DIGEST,
        )
        == 0
    )


def test_free_adaptive_digest_is_allowed():
    service = EntitlementService()

    decision = service.check(
        "account_1",
        FEATURE_ADAPTIVE_DIGEST,
    )

    assert decision.allowed


def test_free_multi_device_is_blocked():
    service = EntitlementService()

    decision = service.check(
        "account_1",
        FEATURE_MULTI_DEVICE,
    )

    assert not decision.allowed


def test_plan_can_upgrade_without_repairing_device():
    service = EntitlementService(
        free_mobile_digest_limit=0
    )

    before = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert not before.allowed

    service.set_plan(
        "account_1",
        SubscriptionPlan.PRO,
    )

    after = service.check(
        "account_1",
        FEATURE_MOBILE_DIGEST,
    )

    assert after.allowed
