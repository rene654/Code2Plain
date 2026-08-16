from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


DISPATCHER = (
    ROOT
    / "src"
    / "code2plain"
    / "notifications"
    / "dispatcher.py"
)


def test_dispatcher_builds_message_automatically():
    text = DISPATCHER.read_text()

    assert (
        "_build_message"
        in text
    )

    assert (
        "provider.send"
        in text
    )


def test_no_manual_message_composition_required():
    text = DISPATCHER.read_text()

    assert (
        "manual_message"
        not in text
    )

    assert (
        "prompt_user"
        not in text
    )
