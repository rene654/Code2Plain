import sqlite3

from code2plain.devices import (
    NtfyEndpointRegistry,
)


def test_ntfy_schema_has_no_phone_source_or_subscription(
    tmp_path,
):

    path = (
        tmp_path
        / "devices.db"
    )

    NtfyEndpointRegistry(
        path
    )


    connection = sqlite3.connect(
        path
    )


    rows = connection.execute(
        """
        PRAGMA table_info(
            ntfy_endpoints
        )
        """
    ).fetchall()


    connection.close()


    columns = {
        row[1]
        for row in rows
    }


    forbidden = {
        "phone",
        "phone_number",
        "source_code",
        "code",
        "plan",
        "premium",
        "subscription",
    }


    assert columns.isdisjoint(
        forbidden
    )
