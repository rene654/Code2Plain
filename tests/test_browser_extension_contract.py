import json
from pathlib import Path


ROOT = Path(
    "browser_extension"
)

MANIFEST = json.loads(
    (
        ROOT / "manifest.json"
    ).read_text(
        encoding="utf-8"
    )
)

CONTENT = (
    ROOT / "chatgpt.js"
).read_text(
    encoding="utf-8"
)

BACKGROUND = (
    ROOT / "background.js"
).read_text(
    encoding="utf-8"
)


def test_extension_only_targets_chatgpt_for_now():
    matches = (
        MANIFEST[
            "content_scripts"
        ][0]["matches"]
    )

    assert matches == [
        "https://chatgpt.com/*"
    ]


def test_adapter_requires_assistant_role():
    assert (
        'data-message-author-role="assistant"'
        in CONTENT
    )

    assert (
        "CODE2PLAIN_ANALYZE"
        in CONTENT
    )


def test_extension_uses_auto_learning_api():
    assert (
        "/v1/auto-learn"
        in BACKGROUND
    )


def test_inline_learning_not_popup():
    assert (
        "code2plain-learning"
        in CONTENT
    )

    assert (
        "window.open"
        not in CONTENT
    )


def test_extension_limits_itself_to_ai_code_blocks():
    assert (
        "pre code"
        in CONTENT
    )

    assert (
        "assistantMessage"
        in CONTENT
    )


def test_backend_address_is_configurable():
    assert (
        "code2plainApiBase"
        in BACKGROUND
    )

    assert (
        "chrome.storage.local"
        in BACKGROUND
    )


def test_extension_fails_silently_when_backend_is_offline():
    assert (
        "ok: false"
        in BACKGROUND
    )
