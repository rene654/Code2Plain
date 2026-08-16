from __future__ import annotations

from pathlib import Path

from code2plain.devices import (
    DeviceRegistry,
    NtfyEndpointRegistry,
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
    NotificationDispatcher,
    NtfyNotificationProvider,
)


DATABASE = Path(
    "code2plain_devices.db"
)

LEARNER_ID = (
    "learner_iphone_demo"
)

ACCOUNT_ID = (
    "account_iphone_demo"
)


# ------------------------------------------------------------
# 1. Simulate real Code2Plain learning observations
# ------------------------------------------------------------

tracker = SessionLearningTracker(
    learner_id=LEARNER_ID,
    session_id="iphone_real_session",
)


tracker.observe_explanation(
    {
        "sections": [
            {
                "concept":
                    "IMPORT"
            },
            {
                "concept":
                    "FILTER"
            },
            {
                "concept":
                    "HANDLE ERROR"
            },
            {
                "concept":
                    "AGGREGATE"
            },
        ]
    }
)


# ------------------------------------------------------------
# 2. Build adaptive learning digest
# ------------------------------------------------------------

digest = (
    AdaptiveSessionDigestBuilder(
        "es"
    )
    .build(
        tracker.session,
        tracker.profile,
    )
)


# ------------------------------------------------------------
# 3. Commercial authorization
# ------------------------------------------------------------

entitlements = (
    EntitlementService()
)

entitlements.set_plan(
    ACCOUNT_ID,
    SubscriptionPlan.PRO,
)


decision = entitlements.check(
    ACCOUNT_ID,
    "mobile_digest",
)


if not decision.allowed:
    raise SystemExit(
        "Mobile digest entitlement denied."
    )


# ------------------------------------------------------------
# 4. Physical delivery provider
# ------------------------------------------------------------

device_registry = DeviceRegistry(
    DATABASE
)

ntfy_registry = NtfyEndpointRegistry(
    DATABASE
)

provider = NtfyNotificationProvider(
    ntfy_registry
)


dispatcher = NotificationDispatcher(
    device_registry,
    provider,
    entitlements,
)


# ------------------------------------------------------------
# 5. Full product dispatch
# ------------------------------------------------------------

results = (
    dispatcher.dispatch_digest(
        LEARNER_ID,
        digest,
        account_id=ACCOUNT_ID,
    )
)


provider.close()


if not results:

    raise SystemExit(
        "No notification was dispatched. "
        "Run setup_learning_digest_iphone.py first."
    )


successful = [
    result
    for result in results
    if result.success
]


print()
print(
    "========================================"
)
print(
    " CODE2PLAIN — LEARNING DIGEST RESULT"
)
print(
    "========================================"
)

print()
print(
    "Learner:",
    LEARNER_ID
)

print(
    "Account plan:",
    entitlements.get_plan(
        ACCOUNT_ID
    ).value
)

print(
    "Entitlement allowed:",
    decision.allowed
)

print()
print(
    "Focus concept:",
    digest.focus_concept
)

print(
    "Focus status:",
    digest.focus_status
)

print(
    "Focus score:",
    digest.focus_score
)

print()

print(
    "Key learning:"
)

print(
    digest.key_learning
)

print()

for result in results:

    print(
        "Provider:",
        result.provider
    )

    print(
        "Device:",
        result.device_id
    )

    print(
        "Success:",
        result.success
    )

    print(
        "Message ID:",
        result.message_id
    )

    if result.error:
        print(
            "Error:",
            result.error
        )


if not successful:
    raise SystemExit(
        1
    )


print()
print(
    "FULL LEARNING → iPHONE PIPELINE: PASS"
)

print()
