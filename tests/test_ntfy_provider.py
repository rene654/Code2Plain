import json

import httpx

from code2plain.devices import (
    NtfyEndpointRegistry,
)
from code2plain.notifications import (
    NotificationMessage,
    NtfyNotificationProvider,
)


def test_ntfy_provider_posts_unicode_json(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    registry.register(
        device_id="device_1",
        topic="code2plain-test-topic",
    )

    captured = {}


    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured[
            "request"
        ] = request

        return httpx.Response(
            200,
            json={
                "id":
                    "ntfy-msg-1"
            },
        )


    provider = NtfyNotificationProvider(
        registry,
        client=httpx.Client(
            transport=(
                httpx.MockTransport(
                    handler
                )
            )
        ),
    )


    result = provider.send(
        NotificationMessage(
            device_id="device_1",
            title=(
                "Code2Plain · "
                "Sesión completada"
            ),
            body=(
                "Hoy tu prioridad "
                "es manejo de errores."
            ),
        )
    )


    assert result.success

    assert (
        result.provider
        == "ntfy"
    )

    assert (
        result.message_id
        == "ntfy-msg-1"
    )


    request = captured[
        "request"
    ]


    assert (
        str(
            request.url
        )
        ==
        "https://ntfy.sh/"
    )

    assert (
        request.method
        == "POST"
    )


    payload = json.loads(
        request.content.decode(
            "utf-8"
        )
    )


    assert (
        payload[
            "topic"
        ]
        ==
        "code2plain-test-topic"
    )


    assert (
        payload[
            "title"
        ]
        ==
        "Code2Plain · "
        "Sesión completada"
    )


    assert (
        payload[
            "message"
        ]
        ==
        "Hoy tu prioridad "
        "es manejo de errores."
    )


    assert (
        payload[
            "priority"
        ]
        == 3
    )


def test_missing_ntfy_endpoint_blocks_delivery(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    provider = NtfyNotificationProvider(
        registry
    )

    result = provider.send(
        NotificationMessage(
            device_id="missing",
            title="Code2Plain",
            body="Digest ready.",
        )
    )

    provider.close()

    assert not result.success


def test_revoked_ntfy_endpoint_blocks_delivery(
    tmp_path,
):

    registry = (
        NtfyEndpointRegistry(
            tmp_path
            / "devices.db"
        )
    )

    registry.register(
        device_id="device_1",
        topic="secret-topic",
    )

    registry.revoke(
        "device_1"
    )

    provider = NtfyNotificationProvider(
        registry
    )

    result = provider.send(
        NotificationMessage(
            device_id="device_1",
            title="Code2Plain",
            body="Digest ready.",
        )
    )

    provider.close()

    assert not result.success
