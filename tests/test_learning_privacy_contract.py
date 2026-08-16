from dataclasses import fields

from code2plain.learning.models import (
    LearningProfile,
)


def test_profile_has_no_phone_number():
    names = {
        field.name
        for field in fields(
            LearningProfile
        )
    }

    assert "phone" not in names
    assert "phone_number" not in names
    assert "mobile_number" not in names


def test_profile_has_no_push_tokens():
    names = {
        field.name
        for field in fields(
            LearningProfile
        )
    }

    assert "push_token" not in names
    assert "device_token" not in names
