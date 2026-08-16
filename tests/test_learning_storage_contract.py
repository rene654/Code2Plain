import sqlite3

from code2plain.learning import (
    LearningProfileStore,
)


def test_database_contains_only_learning_tables(
    tmp_path,
):
    path = (
        tmp_path
        / "learning.db"
    )

    LearningProfileStore(
        path
    )

    connection = sqlite3.connect(
        path
    )

    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    names = {
        row[0]
        for row in rows
    }

    assert (
        "learning_profiles"
        in names
    )

    assert (
        "learning_concepts"
        in names
    )


def test_learning_concepts_schema_has_no_sensitive_fields(
    tmp_path,
):
    path = (
        tmp_path
        / "learning.db"
    )

    LearningProfileStore(
        path
    )

    connection = sqlite3.connect(
        path
    )

    rows = connection.execute(
        """
        PRAGMA table_info(
            learning_concepts
        )
        """
    ).fetchall()

    connection.close()

    columns = {
        row[1]
        for row in rows
    }

    forbidden = {
        "source_code",
        "phone",
        "phone_number",
        "mobile_number",
        "push_token",
        "device_token",
    }

    assert (
        columns.isdisjoint(
            forbidden
        )
    )
