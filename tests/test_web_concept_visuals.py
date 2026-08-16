from pathlib import Path


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

CSS = (
    ROOT
    / "src"
    / "code2plain"
    / "web"
    / "static"
    / "styles.css"
)


def test_concept_visual_container_exists():
    text = HTML.read_text()

    assert (
        'id="conceptVisual"'
        in text
    )


def test_visual_renderer_supports_core_concepts():
    text = JS.read_text()

    for concept in (
        "IMPORT",
        "LOAD DATA",
        "FILTER",
        "AGGREGATE",
        "EXPORT",
    ):
        assert (
            f'concept === "{concept}"'
            in text
        )


def test_visual_system_has_learning_animations():
    text = CSS.read_text()

    assert (
        "@keyframes filteredOut"
        in text
    )

    assert (
        "@keyframes surviveRow"
        in text
    )

    assert (
        "@keyframes aggregateResult"
        in text
    )
