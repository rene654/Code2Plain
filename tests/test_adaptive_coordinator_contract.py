from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


def test_coordinator_uses_adaptive_digest_automatically():
    text = (
        ROOT
        / "src"
        / "code2plain"
        / "learning"
        / "session_coordinator.py"
    ).read_text()

    assert (
        "AdaptiveSessionDigestBuilder"
        in text
    )

    assert (
        "from code2plain.learning.digest import (\n"
        "    SessionDigestBuilder,"
        not in text
    )


def test_user_does_not_select_focus_manually():
    text = (
        ROOT
        / "src"
        / "code2plain"
        / "learning"
        / "adaptive_digest.py"
    ).read_text()

    assert (
        "_choose_adaptive_focus"
        in text
    )

    assert (
        "manual_focus"
        not in text
    )
