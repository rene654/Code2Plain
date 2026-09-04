from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def test_owner_mode_has_explicit_exit_flow():
    source = _source()

    start = source.index(
        "async function exitOwner()"
    )
    end = source.index(
        "async function handleOwnerAccess()",
        start,
    )

    exit_source = source[start:end]

    assert (
        '"code2plain.owner_token"'
        in exit_source
    )
    assert (
        "window.localStorage.removeItem"
        in exit_source
    )
    assert (
        'ownerAccessButton.textContent ='
        in exit_source
    )
    assert '"Owner"' in exit_source
    assert (
        "ownerAccessButton.classList.remove"
        in exit_source
    )
    assert (
        "await startOrRestoreDemo();"
        in exit_source
    )
    assert (
        "updateDemoTimer();"
        in exit_source
    )


def test_owner_button_switches_between_login_and_exit():
    source = _source()

    start = source.index(
        "async function handleOwnerAccess()"
    )
    end = source.index(
        "async function loginOwner()",
        start,
    )

    handler_source = source[start:end]

    assert "if (ownerToken)" in handler_source
    assert "await exitOwner();" in handler_source
    assert "await loginOwner();" in handler_source

    assert (
        '''ownerAccessButton.addEventListener(
        "click",
        handleOwnerAccess
    );'''
        in source
    )

    assert '"Exit Owner"' in source
