from code2plain.notifications import (
    APNsNotificationProvider,
    NtfyNotificationProvider,
)
from code2plain.notifications.provider import (
    NotificationProvider,
)


def test_apns_and_ntfy_share_provider_contract():

    assert issubclass(
        APNsNotificationProvider,
        NotificationProvider,
    )

    assert issubclass(
        NtfyNotificationProvider,
        NotificationProvider,
    )
