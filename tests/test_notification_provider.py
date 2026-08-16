from code2plain.notifications import (
    InMemoryNotificationProvider,
    NotificationMessage,
)


def test_memory_provider_records_message():
    provider = (
        InMemoryNotificationProvider()
    )

    message = NotificationMessage(
        device_id="device_1",
        title="Code2Plain",
        body="Learning summary ready.",
    )

    result = provider.send(
        message
    )

    assert result.success
    assert result.provider == "memory"
    assert result.message_id

    assert provider.sent == [
        message
    ]
