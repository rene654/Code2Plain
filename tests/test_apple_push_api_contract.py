from code2plain.api.apple_push import (
    ApplePushRegistrationRequest,
)


def test_registration_request_contains_required_fields():

    request = (
        ApplePushRegistrationRequest(
            pairing_token="pair123",
            apns_token="apns123",
            bundle_id="com.code2plain.app",
        )
    )

    assert (
        request.pairing_token
        == "pair123"
    )

    assert (
        request.apns_token
        == "apns123"
    )

    assert (
        request.environment
        == "sandbox"
    )


def test_registration_request_has_no_subscription_state():

    fields = (
        ApplePushRegistrationRequest
        .model_fields
    )

    assert "plan" not in fields
    assert "premium" not in fields
    assert "subscription" not in fields
