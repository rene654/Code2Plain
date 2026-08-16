from dataclasses import fields

from code2plain.devices.models import (
    DeviceRecord,
)
from code2plain.entitlements.models import (
    EntitlementDecision,
)


def test_device_record_does_not_store_plan():
    names = {
        field.name
        for field in fields(
            DeviceRecord
        )
    }

    assert "plan" not in names
    assert "subscription" not in names
    assert "premium" not in names


def test_entitlement_decision_has_no_device_token():
    names = {
        field.name
        for field in fields(
            EntitlementDecision
        )
    }

    assert "device_token" not in names
    assert "push_token" not in names


def test_entitlement_is_account_scoped():
    names = {
        field.name
        for field in fields(
            EntitlementDecision
        )
    }

    assert "account_id" in names
    assert "feature" in names
    assert "allowed" in names
