from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt


OWNER_SESSION_HOURS = 12


@dataclass(frozen=True)
class OwnerSession:
    token: str
    expires_at: str


@dataclass(frozen=True)
class OwnerSessionStatus:
    valid: bool
    expires_at: str | None


class OwnerAccessService:
    """
    Validates the private owner credential and issues
    short-lived owner session tokens.

    The raw owner credential is used only to create
    a session and is never stored in the browser.
    """

    def __init__(
        self,
        *,
        secret: str | None = None,
        signing_secret: str | None = None,
        session_hours: int = OWNER_SESSION_HOURS,
    ) -> None:
        self.secret = (
            secret
            if secret is not None
            else os.environ.get(
                "CODE2PLAIN_OWNER_SECRET",
                "",
            )
        )

        self.signing_secret = (
            signing_secret
            if signing_secret is not None
            else os.environ.get(
                "CODE2PLAIN_OWNER_SIGNING_SECRET",
                "",
            )
        )

        self.session_hours = session_hours

    @property
    def configured(self) -> bool:
        return bool(
            self.secret
            and self.signing_secret
        )

    def verify_credential(
        self,
        credential: str | None,
    ) -> bool:
        if (
            not self.secret
            or not credential
        ):
            return False

        expected = hashlib.sha256(
            self.secret.encode("utf-8")
        ).digest()

        supplied = hashlib.sha256(
            credential.encode("utf-8")
        ).digest()

        return hmac.compare_digest(
            expected,
            supplied,
        )

    def issue_session(
        self,
        credential: str,
    ) -> OwnerSession | None:
        if not self.verify_credential(
            credential
        ):
            return None

        if not self.signing_secret:
            return None

        now = datetime.now(
            UTC
        )

        expires = (
            now
            + timedelta(
                hours=self.session_hours
            )
        )

        payload = {
            "kind":
                "code2plain-owner",
            "iat":
                int(now.timestamp()),
            "exp":
                int(expires.timestamp()),
        }

        token = jwt.encode(
            payload,
            self.signing_secret,
            algorithm="HS256",
        )

        return OwnerSession(
            token=token,
            expires_at=(
                expires.isoformat()
            ),
        )

    def verify_session(
        self,
        token: str | None,
    ) -> OwnerSessionStatus:
        if (
            not token
            or not self.signing_secret
        ):
            return OwnerSessionStatus(
                valid=False,
                expires_at=None,
            )

        try:
            payload = jwt.decode(
                token,
                self.signing_secret,
                algorithms=["HS256"],
            )
        except jwt.PyJWTError:
            return OwnerSessionStatus(
                valid=False,
                expires_at=None,
            )

        if (
            payload.get("kind")
            != "code2plain-owner"
        ):
            return OwnerSessionStatus(
                valid=False,
                expires_at=None,
            )

        expires = datetime.fromtimestamp(
            int(payload["exp"]),
            tz=UTC,
        )

        return OwnerSessionStatus(
            valid=True,
            expires_at=(
                expires.isoformat()
            ),
        )


owner_access_service = OwnerAccessService()
