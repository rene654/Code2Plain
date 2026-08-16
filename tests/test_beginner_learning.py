from pathlib import Path

from code2plain.service import Code2PlainService


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

HTML = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "index.html"
)

JS = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "static"
    / "app.js"
)


def test_learn_mode_uses_beginner_language():
    result = (
        Code2PlainService()
        .explain_code(
            'late_orders = '
            'df[df["status"] == "Late"]'
        )
    )

    learn = (
        result["sections"][0]
        ["learning_modes"]["learn"]
    )

    assert (
        learn["primary_label"]
        == "EN PALABRAS SIMPLES"
    )

    assert (
        learn["secondary_label"]
        == "IDEA CLAVE"
    )

    assert (
        "conserva solamente"
        in learn[
            "primary"
        ].lower()
    )


def test_filter_key_idea_is_beginner_friendly():
    result = (
        Code2PlainService()
        .explain_code(
            'late_orders = '
            'df[df["status"] == "Late"]'
        )
    )

    learn = (
        result["sections"][0]
        ["learning_modes"]["learn"]
    )

    assert (
        "quedarte solamente"
        in learn[
            "secondary"
        ].lower()
    )


def test_program_flow_container_exists():
    text = HTML.read_text()

    assert (
        'id="programFlow"'
        in text
    )


def test_program_flow_is_connected_to_sections():
    text = JS.read_text()

    assert (
        "renderProgramFlow"
        in text
    )

    assert (
        "updateProgramFlow"
        in text
    )

    assert (
        "data-flow-index"
        in text
    )
