from dataclasses import fields

from code2plain.notifications.models import (
    NotificationMessage,
)


def test_notification_message_has_no_phone_number():
    names = {
        field.name
        for field in fields(
            NotificationMessage
        )
    }

    forbidden = {
        "phone",
        "phone_number",
        "mobile_number",
        "telephone_number",
    }

    assert names.isdisjoint(
        forbidden
    )


def test_notification_message_has_no_source_code_field():
    names = {
        field.name
        for field in fields(
            NotificationMessage
        )
    }

    assert "source_code" not in names
    assert "code" not in names
