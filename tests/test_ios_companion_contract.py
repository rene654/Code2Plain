from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


IOS = (
    ROOT
    / "ios"
    / "Code2PlainCompanion"
    / "Code2PlainCompanion"
)


def read(
    filename,
):
    return (
        IOS
        / filename
    ).read_text()


def test_ios_companion_requests_notification_permission():

    text = read(
        "NotificationManager.swift"
    )

    assert (
        "requestAuthorization"
        in text
    )

    assert (
        "registerForRemoteNotifications"
        in text
    )


def test_ios_companion_handles_apns_token():

    text = read(
        "AppDelegate.swift"
    )

    assert (
        "didRegisterForRemoteNotificationsWithDeviceToken"
        in text
    )


def test_ios_companion_does_not_contain_premium_state():

    combined = "\n".join(
        path.read_text()
        for path in IOS.glob(
            "*.swift"
        )
    ).lower()

    assert "premium=true" not in combined
    assert "plan=pro" not in combined


def test_ios_companion_has_no_source_code_payload():

    text = read(
        "APIClient.swift"
    )

    assert "sourceCode" not in text
    assert "source_code" not in text
