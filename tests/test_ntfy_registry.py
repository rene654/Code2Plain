from code2plain.devices import (
    NtfyEndpointRegistry,
)


def test_topic_is_generated_with_high_entropy_prefix(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    endpoint = registry.register(
        device_id="device_1"
    )

    assert (
        endpoint.topic.startswith(
            "code2plain-"
        )
    )

    assert len(
        endpoint.topic
    ) > 30

    assert endpoint.is_active


def test_ntfy_endpoint_can_be_revoked(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    registry.register(
        device_id="device_1"
    )

    endpoint = registry.revoke(
        "device_1"
    )

    assert not endpoint.is_active


def test_registering_same_device_rotates_topic(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    first = registry.register(
        device_id="device_1"
    )

    second = registry.register(
        device_id="device_1"
    )

    assert (
        first.topic
        != second.topic
    )

    assert second.is_active
