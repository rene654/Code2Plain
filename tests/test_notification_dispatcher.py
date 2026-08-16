from datetime import (
    datetime,
    timedelta,
    timezone,
)

from code2plain.devices import (
    DeviceRegistry,
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
                },
                {
                    "concept":
                        "AGGREGATE"
                },
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
    learner_id,
    minute=0,
):
    pairing = (
        registry.create_pairing_request(
            learner_id,
            now=(
                BASE
                + timedelta(
                    minutes=minute
                )
            ),
        )
    )

    return (
        registry.redeem_pairing_token(
            pairing.token,
            now=(
                BASE
                + timedelta(
                    minutes=minute + 1
                )
            ),
        )
    )


def test_dispatches_to_active_device(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    device = pair_device(
        registry,
        "learner_1",
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = (
        NotificationDispatcher(
            registry,
            provider,
        )
    )

    results = (
        dispatcher.dispatch_digest(
            "learner_1",
            make_digest(),
        )
    )

    assert len(results) == 1
    assert results[0].success

    assert (
        provider.sent[0].device_id
        == device.device_id
    )


def test_revoked_device_receives_nothing(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    device = pair_device(
        registry,
        "learner_1",
    )

    registry.revoke_device(
        device.device_id,
        now=(
            BASE
            + timedelta(
                minutes=3
            )
        ),
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = (
        NotificationDispatcher(
            registry,
            provider,
        )
    )

    results = (
        dispatcher.dispatch_digest(
            "learner_1",
            make_digest(),
        )
    )

    assert results == []
    assert provider.sent == []


def test_multiple_active_devices_receive_digest(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry,
        "learner_1",
        minute=0,
    )

    pair_device(
        registry,
        "learner_1",
        minute=3,
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = (
        NotificationDispatcher(
            registry,
            provider,
        )
    )

    results = (
        dispatcher.dispatch_digest(
            "learner_1",
            make_digest(),
        )
    )

    assert len(results) == 2
    assert len(provider.sent) == 2


def test_other_learner_device_is_not_notified(
    tmp_path,
):
    registry = DeviceRegistry(
        tmp_path / "devices.db"
    )

    pair_device(
        registry,
        "learner_1",
        minute=0,
    )

    pair_device(
        registry,
        "learner_2",
        minute=3,
    )

    provider = (
        InMemoryNotificationProvider()
    )

    dispatcher = (
        NotificationDispatcher(
            registry,
            provider,
        )
    )

    results = (
        dispatcher.dispatch_digest(
            "learner_1",
            make_digest(),
        )
    )

    assert len(results) == 1
    assert len(provider.sent) == 1
