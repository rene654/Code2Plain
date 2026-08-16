from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


def test_session_end_module_has_automatic_detector():
    text = (
        ROOT
        / "src"
        / "code2plain"
        / "learning"
        / "session_end.py"
    ).read_text()

    assert (
        "AutomaticSessionEndDetector"
        in text
    )

    assert (
        "READY_TO_CLOSE"
        in text
    )


def test_coordinator_builds_digest_without_manual_finish():
    text = (
        ROOT
        / "src"
        / "code2plain"
        / "learning"
        / "session_coordinator.py"
    ).read_text()

    assert (
        "digest_builder.build"
        in text
    )

    assert (
        "profile_store.save"
        in text
    )


def test_no_required_manual_finish_button_contract():
    text = (
        ROOT
        / "src"
        / "code2plain"
        / "learning"
        / "session_coordinator.py"
    ).read_text()

    assert (
        "finish_button"
        not in text
    )

    assert (
        "manual_finish_required"
        not in text
    )
