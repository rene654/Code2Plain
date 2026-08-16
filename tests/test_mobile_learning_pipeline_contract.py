from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


SCRIPT = (
    ROOT
    / "scripts"
    / "send_learning_digest_iphone.py"
)


def test_physical_script_uses_adaptive_digest():

    text = SCRIPT.read_text()

    assert (
        "AdaptiveSessionDigestBuilder"
        in text
    )


def test_physical_script_uses_entitlements():

    text = SCRIPT.read_text()

    assert (
        "EntitlementService"
        in text
    )

    assert (
        "SubscriptionPlan"
        in text
    )


def test_physical_script_uses_dispatcher():

    text = SCRIPT.read_text()

    assert (
        "NotificationDispatcher"
        in text
    )


def test_physical_script_uses_ntfy_only_as_adapter():

    text = SCRIPT.read_text()

    assert (
        "NtfyNotificationProvider"
        in text
    )

    assert (
        "AdaptiveSessionDigestBuilder"
        in text
    )
