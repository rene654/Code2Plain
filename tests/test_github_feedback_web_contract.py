from pathlib import Path


HTML = Path(
    "src/code2plain/web/index.html"
).read_text(
    encoding="utf-8"
)

JS = Path(
    "src/code2plain/web/static/app.js"
).read_text(
    encoding="utf-8"
)


def test_failure_feedback_ui_exists():
    assert "compactFailureSection" in HTML
    assert "compactFailureText" in HTML
    assert "compactFailureMeta" in HTML


def test_failure_feedback_renderer_exists():
    assert "showGitHubFeedback" in JS
    assert "feedback.what_failed" in JS
    assert "feedback.where_to_look" in JS
    assert "feedback.concept" in JS
