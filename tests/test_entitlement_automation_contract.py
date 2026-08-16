from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


DISPATCHER = (
    ROOT
    / "src"
    / "code2plain"
    / "notifications"
    / "dispatcher.py"
)


def test_dispatcher_checks_entitlement_automatically():
    text = DISPATCHER.read_text()

    assert (
        "entitlement_service.check"
        in text
    )

    assert (
        "FEATURE_MOBILE_DIGEST"
        in text
    )


def test_no_user_confirmation_required_per_digest():
    text = DISPATCHER.read_text()

    forbidden = (
        "confirm_purchase",
        "ask_user_permission",
        "manual_entitlement_check",
    )

    assert all(
        item not in text
        for item in forbidden
    )
