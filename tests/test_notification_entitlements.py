from datetime import (
    datetime,
    timedelta,
    timezone,
)

import pytest

from code2plain.devices import (
    DeviceRegistry,
)
from code2plain.entitlements import (
    EntitlementService,
    SubscriptionPlan,
)
from code2plain.learning import (
    AdaptiveSessionDigestBuilder,
    SessionLearningTracker,
)
from code2plain.notifications import (
    InMemoryNotificationProvider,
    NotificationDispatcher,
)


BASE = datetime(
    2026,
    8,
    16,
    12,
    0,
    tzinfo=timezone.utc,
)


def make_digest():
    tracker = SessionLearningTracker(
        learner_id="learner_1",
        session_id="session_1",
    )

    tracker.observe_explanation(
        {
            "sections": [
                {
                    "concept":
                        "FILTER"
                }
            ]
        },
        observed_at=BASE,
    )

    return (
        AdaptiveSessionDigestBuilder(
            "es"
        )
        .build(
            tracker.session,
            tracker.profile,
        )
    )


def pair_device(
    registry,
):
    pairing = (
        registry.create_pairing_request(
            "learner_1",
            now=BASE,
        )
    )

    return registry.redeem_pairing_token(
        pairing.token,
        now=(
            BASE
            + timedelta(
                minutes=1
            )
        ),
    )


def test_pairing_does_not_bypass_entitlement(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry
    )

    entitlements = EntitlementService(
        free_mobile_digest_limit=0
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = NotificationDispatcher(
        registry,
        provider,
        entitlements,
    )

    results = dispatcher.dispatch_digest(
        "learner_1",
        make_digest(),
        account_id="account_1",
    )

    assert results == []
    assert provider.sent == []


def test_pro_account_receives_digest(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry
    )

    entitlements = EntitlementService()

    entitlements.set_plan(
        "account_1",
        SubscriptionPlan.PRO,
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = NotificationDispatcher(
        registry,
        provider,
        entitlements,
    )

    results = dispatcher.dispatch_digest(
        "learner_1",
        make_digest(),
        account_id="account_1",
    )

    assert len(results) == 1
    assert results[0].success
    assert len(provider.sent) == 1


def test_free_digest_consumes_one_usage(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry
    )

    entitlements = EntitlementService(
        free_mobile_digest_limit=2
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = NotificationDispatcher(
        registry,
        provider,
        entitlements,
    )

    dispatcher.dispatch_digest(
        "learner_1",
        make_digest(),
        account_id="account_1",
    )

    assert (
        entitlements.usage_count(
            "account_1",
            "mobile_digest",
        )
        == 1
    )


def test_missing_account_is_rejected_when_gate_enabled(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry
    )

    dispatcher = NotificationDispatcher(
        registry,
        InMemoryNotificationProvider(),
        EntitlementService(),
    )

    with pytest.raises(
        ValueError,
        match="account_id is required",
    ):
        dispatcher.dispatch_digest(
            "learner_1",
            make_digest(),
        )


def test_legacy_dispatcher_still_works_without_gate(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = NotificationDispatcher(
        registry,
        provider,
    )

    results = dispatcher.dispatch_digest(
        "learner_1",
        make_digest(),
    )

    assert len(results) == 1
