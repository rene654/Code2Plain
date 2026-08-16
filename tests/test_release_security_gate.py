from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


def test_local_device_database_is_gitignored():

    text = (
        ROOT
        / ".gitignore"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "code2plain_devices.db"
        in text
    )


def test_apple_private_keys_are_gitignored():

    text = (
        ROOT
        / ".gitignore"
    ).read_text(
        encoding="utf-8"
    )

    assert "*.p8" in text


def test_security_gate_exists():

    path = (
        ROOT
        / "scripts"
        / "security_release_gate.py"
    )

    assert path.exists()


def test_release_gate_distinguishes_personal_from_public():

    text = (
        ROOT
        / "scripts"
        / "security_release_gate.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "PERSONAL BETA RELEASE GATE"
        in text
    )

    assert (
        "Public/commercial production"
        in text
    )
