from dataclasses import fields

from code2plain.devices.push_models import (
    ApplePushEndpoint,
)
from code2plain.notifications.apns_auth import (
    APNsAuthConfig,
)


def test_private_key_is_not_stored_on_device_endpoint():
    names = {
        field.name
        for field in fields(
            ApplePushEndpoint
        )
    }

    assert "private_key" not in names
    assert "team_id" not in names
    assert "key_id" not in names


def test_auth_config_references_key_file_not_key_contents():
    names = {
        field.name
        for field in fields(
            APNsAuthConfig
        )
    }

    assert (
        "private_key_path"
        in names
    )

    assert (
        "private_key"
        not in names
    )
