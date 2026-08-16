import sqlite3

from code2plain.devices import (
    DeviceRegistry,
)


def test_device_schema_has_no_phone_number(
    tmp_path,
):
    path = (
        tmp_path
        / "devices.db"
    )

    DeviceRegistry(
        path
    )

    connection = sqlite3.connect(
        path
    )

    rows = connection.execute(
        """
        PRAGMA table_info(devices)
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
        "telephone_number",
    }

    assert columns.isdisjoint(
        forbidden
    )


def test_raw_pairing_token_is_not_stored(
    tmp_path,
):
    path = (
        tmp_path
        / "devices.db"
    )

    registry = DeviceRegistry(
        path
    )

    request = registry.create_pairing_request(
        "learner_1"
    )

    connection = sqlite3.connect(
        path
    )

    row = connection.execute(
        """
        SELECT token_hash
        FROM pairing_requests
        WHERE pairing_id = ?
        """,
        (
            request.pairing_id,
        ),
    ).fetchone()

    connection.close()

    assert row is not None

    assert (
        row[0]
        != request.token
    )


def test_pairing_table_has_no_phone_fields(
    tmp_path,
):
    path = (
        tmp_path
        / "devices.db"
    )

    DeviceRegistry(
        path
    )

    connection = sqlite3.connect(
        path
    )

    rows = connection.execute(
        """
        PRAGMA table_info(
            pairing_requests
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
        "telephone_number",
    }

    assert columns.isdisjoint(
        forbidden
    )
