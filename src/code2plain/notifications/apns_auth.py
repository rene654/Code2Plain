from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    datetime,
    timezone,
)
from pathlib import Path

import jwt


@dataclass(frozen=True)
class APNsAuthConfig:
    key_id: str
    team_id: str
    private_key_path: Path

    def __post_init__(self) -> None:
        if not self.key_id.strip():
            raise ValueError(
                "key_id cannot be empty"
            )

        if not self.team_id.strip():
            raise ValueError(
                "team_id cannot be empty"
            )

        if not Path(
            self.private_key_path
        ).exists():
            raise ValueError(
                "APNs private key file does not exist"
            )


class APNsJWTProvider:
    """
    Creates Apple provider authentication tokens.

    The .p8 private key remains outside application
    source control and is loaded only when generating
    the signed JWT.
    """

    def __init__(
        self,
        config: APNsAuthConfig,
    ) -> None:
        self.config = config


    def create_token(
        self,
        *,
        now: datetime | None = None,
    ) -> str:

        timestamp = (
            now
            or datetime.now(
                timezone.utc
            )
        )

        private_key = (
            Path(
                self.config.private_key_path
            )
            .read_text()
        )

        return jwt.encode(
            {
                "iss":
                    self.config.team_id,

                "iat":
                    int(
                        timestamp.timestamp()
                    ),
            },
            private_key,
            algorithm="ES256",
            headers={
                "kid":
                    self.config.key_id,
            },
        )
