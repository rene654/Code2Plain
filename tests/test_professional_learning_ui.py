from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def test_professional_ui_system_is_present():
    source = _source()

    assert (
        "CODE2PLAIN PROFESSIONAL UI SYSTEM"
        in source
    )

    assert "--c2p-navy:" in source
    assert "--c2p-cyan:" in source
    assert "--c2p-ivory:" in source
    assert "--c2p-shadow:" in source


def test_professional_ui_has_real_responsive_breakpoints():
    source = _source()

    assert "@media (max-width: 1100px)" in source
    assert "@media (max-width: 900px)" in source
    assert "@media (max-width: 640px)" in source
    assert "@media (max-width: 390px)" in source


def test_mobile_workspace_reduces_vertical_waste():
    source = _source()

    professional = source.split(
        "CODE2PLAIN PROFESSIONAL UI SYSTEM",
        1,
    )[1]

    assert "min-height: 250px;" in professional
    assert "min-height: 190px;" in professional
    assert "min-height: 210px;" in professional


def test_mobile_header_handles_access_and_privacy_states():
    source = _source()

    professional = source.split(
        "CODE2PLAIN PROFESSIONAL UI SYSTEM",
        1,
    )[1]

    assert ".owner-access-button" in professional
    assert ".demo-timer" in professional
    assert ".privacy-badge" in professional
    assert "white-space: normal;" in professional


def test_primary_learning_action_has_professional_state_styles():
    source = _source()

    professional = source.split(
        "CODE2PLAIN PROFESSIONAL UI SYSTEM",
        1,
    )[1]

    assert "#learn {" in professional
    assert "#learn:hover:not(:disabled)" in professional
    assert "#learn:disabled" in professional
