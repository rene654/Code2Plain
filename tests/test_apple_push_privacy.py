import sqlite3

from code2plain.devices import (
    ApplePushRegistry,
)


def test_apple_push_schema_has_no_phone_or_source_code(
    tmp_path,
):
    path = (
        tmp_path
        / "devices.db"
    )

    ApplePushRegistry(
        path
    )

    connection = sqlite3.connect(
        path
    )

    rows = connection.execute(
        """
        PRAGMA table_info(
            apple_push_endpoints
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
        "mobile_number",
        "source_code",
        "code",
    }

    assert columns.isdisjoint(
        forbidden
    )
