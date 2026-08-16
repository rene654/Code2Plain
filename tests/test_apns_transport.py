import httpx
import pytest

from code2plain.notifications import (
    APNsDeliveryError,
    APNsRequest,
    HTTP2APNsTransport,
)


class FakeJWTProvider:

    def create_token(
        self,
    ) -> str:

        return "fake.jwt.token"


def make_request(
    *,
    environment="sandbox",
):
    return APNsRequest(
        device_id="device_1",
        apns_token="abc123",
        bundle_id="com.code2plain.app",
        environment=environment,
        title="Code2Plain · Sesión completada",
        body="Hoy aprendiste filtros.",
    )


def test_transport_builds_correct_apns_request():

    captured = {}

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured["request"] = request

        return httpx.Response(
            200,
            headers={
                "apns-id":
                    "apns-id-123"
            },
        )


    transport = HTTP2APNsTransport(
        FakeJWTProvider(),
        client=httpx.Client(
            transport=httpx.MockTransport(
                handler
            ),
            http2=True,
        ),
    )

    message_id = transport.send(
        make_request()
    )

    request = captured[
        "request"
    ]

    assert message_id == "apns-id-123"

    assert (
        str(request.url)
        ==
        "https://api.sandbox.push.apple.com/"
        "3/device/abc123"
    )

    assert (
        request.headers[
            "authorization"
        ]
        == "bearer fake.jwt.token"
    )

    assert (
        request.headers[
            "apns-topic"
        ]
        == "com.code2plain.app"
    )

    assert (
        request.headers[
            "apns-push-type"
        ]
        == "alert"
    )

    assert (
        request.headers[
            "apns-priority"
        ]
        == "10"
    )

    payload = request.read()

    assert (
        b"Code2Plain"
        in payload
    )


def test_production_uses_production_host():

    captured = {}

    def handler(
        request,
    ):
        captured["url"] = str(
            request.url
        )

        return httpx.Response(
            200
        )


    transport = HTTP2APNsTransport(
        FakeJWTProvider(),
        client=httpx.Client(
            transport=httpx.MockTransport(
                handler
            ),
            http2=True,
        ),
    )

    transport.send(
        make_request(
            environment="production"
        )
    )

    assert captured[
        "url"
    ].startswith(
        "https://api.push.apple.com/"
    )


def test_apns_error_reason_is_exposed():

    def handler(
        request,
    ):
        return httpx.Response(
            400,
            json={
                "reason":
                    "BadDeviceToken"
            },
            headers={
                "apns-id":
                    "bad-request-id"
            },
        )


    transport = HTTP2APNsTransport(
        FakeJWTProvider(),
        client=httpx.Client(
            transport=httpx.MockTransport(
                handler
            ),
            http2=True,
        ),
    )

    with pytest.raises(
        APNsDeliveryError
    ) as captured:

        transport.send(
            make_request()
        )

    error = captured.value

    assert error.status_code == 400

    assert (
        error.reason
        == "BadDeviceToken"
    )

    assert (
        error.apns_id
        == "bad-request-id"
    )


def test_invalid_environment_is_rejected():

    transport = HTTP2APNsTransport(
        FakeJWTProvider(),
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request:
                    httpx.Response(200)
            ),
            http2=True,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "Unsupported APNs environment"
        ),
    ):
        transport.send(
            make_request(
                environment="invalid"
            )
        )
