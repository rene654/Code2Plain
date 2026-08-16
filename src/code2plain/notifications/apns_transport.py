from __future__ import annotations

import json
from dataclasses import dataclass

import httpx

from code2plain.notifications.apns_auth import (
    APNsJWTProvider,
)
from code2plain.notifications.apns_provider import (
    APNsRequest,
    APNsTransport,
)


APNS_HOSTS = {
    "sandbox":
        "https://api.sandbox.push.apple.com",

    "production":
        "https://api.push.apple.com",
}


@dataclass(frozen=True)
class APNsTransportResponse:
    status_code: int
    apns_id: str | None
    reason: str | None


class APNsDeliveryError(RuntimeError):

    def __init__(
        self,
        *,
        status_code: int,
        reason: str | None,
        apns_id: str | None,
    ) -> None:

        self.status_code = status_code
        self.reason = reason
        self.apns_id = apns_id

        detail = (
            reason
            or "Unknown APNs error"
        )

        super().__init__(
            f"APNs delivery failed "
            f"({status_code}): {detail}"
        )


class HTTP2APNsTransport(
    APNsTransport
):
    """
    Real APNs provider transport.

    Uses:
    - HTTP/2
    - TLS verification
    - JWT bearer authentication
    - alert push type
    - bundle ID as APNs topic
    """

    def __init__(
        self,
        jwt_provider: APNsJWTProvider,
        *,
        timeout_seconds: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:

        self.jwt_provider = (
            jwt_provider
        )

        self._owns_client = (
            client is None
        )

        self.client = (
            client
            or httpx.Client(
                http2=True,
                timeout=timeout_seconds,
            )
        )


    def close(
        self,
    ) -> None:

        if self._owns_client:
            self.client.close()


    def send(
        self,
        request: APNsRequest,
    ) -> str:

        host = APNS_HOSTS.get(
            request.environment
        )

        if host is None:
            raise ValueError(
                "Unsupported APNs environment"
            )

        provider_token = (
            self.jwt_provider
            .create_token()
        )

        url = (
            f"{host}/3/device/"
            f"{request.apns_token}"
        )

        payload = {
            "aps": {
                "alert": {
                    "title":
                        request.title,

                    "body":
                        request.body,
                }
            }
        }

        headers = {
            "authorization":
                f"bearer {provider_token}",

            "apns-topic":
                request.bundle_id,

            "apns-push-type":
                "alert",

            "apns-priority":
                "10",

            "content-type":
                "application/json",
        }

        response = self.client.post(
            url,
            headers=headers,
            json=payload,
        )

        apns_id = (
            response.headers.get(
                "apns-id"
            )
        )

        reason = None

        if response.status_code != 200:

            try:
                data = response.json()

                reason = data.get(
                    "reason"
                )

            except (
                json.JSONDecodeError,
                ValueError,
            ):
                reason = (
                    response.text
                    or None
                )

            raise APNsDeliveryError(
                status_code=(
                    response.status_code
                ),
                reason=reason,
                apns_id=apns_id,
            )

        return (
            apns_id
            or "apns-accepted"
        )
