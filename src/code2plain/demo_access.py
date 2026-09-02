from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt


DEFAULT_DEMO_MINUTES = 20


@dataclass(frozen=True)
class DemoAccess:
    token: str
    expires_at: str
    duration_minutes: int


@dataclass(frozen=True)
class DemoAccessStatus:
    valid: bool
    user_id: str | None
    expires_at: str | None
    remaining_seconds: int


class DemoAccessService:
    """
    Issues and verifies short-lived demo access tokens.

    The browser cannot change the expiration time because
    the token is cryptographically signed by the server.
    """

    def __init__(
        self,
        *,
        secret: str | None = None,
        duration_minutes: int = DEFAULT_DEMO_MINUTES,
    ) -> None:
        self.secret = (
            secret
            or os.environ.get(
                "CODE2PLAIN_DEMO_SECRET"
            )
            or "development-demo-secret-change-me"
        )

        self.duration_minutes = (
            duration_minutes
        )

    def issue(
        self,
        *,
        user_id: str,
    ) -> DemoAccess:
        now = datetime.now(
            UTC
        )

        expires = (
            now
            + timedelta(
                minutes=self.duration_minutes
            )
        )

        payload = {
            "sub": user_id,
            "kind": "code2plain-demo",
            "iat": int(
                now.timestamp()
            ),
            "exp": int(
                expires.timestamp()
            ),
        }

        token = jwt.encode(
            payload,
            self.secret,
            algorithm="HS256",
        )

        return DemoAccess(
            token=token,
            expires_at=(
                expires.isoformat()
            ),
            duration_minutes=(
                self.duration_minutes
            ),
        )

    def verify(
        self,
        token: str,
    ) -> DemoAccessStatus:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=["HS256"],
            )
        except jwt.PyJWTError:
            return DemoAccessStatus(
                valid=False,
                user_id=None,
                expires_at=None,
                remaining_seconds=0,
            )

        if (
            payload.get("kind")
            != "code2plain-demo"
        ):
            return DemoAccessStatus(
                valid=False,
                user_id=None,
                expires_at=None,
                remaining_seconds=0,
            )

        expires_timestamp = int(
            payload["exp"]
        )

        expires = (
            datetime.fromtimestamp(
                expires_timestamp,
                tz=UTC,
            )
        )

        now = datetime.now(
            UTC
        )

        remaining = max(
            0,
            int(
                (
                    expires
                    - now
                ).total_seconds()
            ),
        )

        return DemoAccessStatus(
            valid=remaining > 0,
            user_id=payload.get(
                "sub"
            ),
            expires_at=(
                expires.isoformat()
            ),
            remaining_seconds=remaining,
        )


demo_access_service = (
    DemoAccessService()
)
