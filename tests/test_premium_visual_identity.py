from pathlib import Path


WEB_APP = Path(
    "src/code2plain/web/app.py"
)


def _source() -> str:
    return WEB_APP.read_text(
        encoding="utf-8"
    )


def _shell() -> str:
    source = _source()

    return source.split(
        "CODE2PLAIN PREMIUM APP SHELL 178C",
        1,
    )[1]


def test_real_app_shell_is_attached_to_main():
    source = _source()

    assert (
        '<main class="app-shell">'
        in source
    )


def test_product_strip_gives_workspace_identity():
    source = _source()

    assert (
        'class="product-strip"'
        in source
    )

    assert (
        "De código a comprensión real."
        in source
    )

    assert (
        "AI-assisted learning workspace"
        in source
    )


def test_code_input_is_rendered_as_editor_shell():
    source = _source()

    assert (
        'class="code-editor-shell"'
        in source
    )

    assert (
        'class="code-editor-toolbar"'
        in source
    )

    assert "main.py" in source
    assert "Python · Ready" in source


def test_reference_blue_navy_palette_is_preserved():
    shell = _shell()

    for color in (
        "#081f46",
        "#04142f",
        "#1165e7",
        "#1aa8d9",
    ):
        assert color in shell


def test_learning_results_have_timeline():
    shell = _shell()

    assert "#results::before" in shell
    assert "counter-reset:" in shell
    assert ".item::before" in shell
    assert "counter-increment:" in shell


def test_mobile_keeps_dark_technology_background():
    shell = _shell()

    assert (
        "@media (max-width: 640px)"
        in shell
    )

    assert "#09285a" in shell
    assert "#04142f" in shell
