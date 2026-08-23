from code2plain.detection import (
    AICodeDetector,
    ContentCandidate,
)


detector = AICodeDetector()


def test_chatgpt_code_is_detected():
    result = detector.detect(
        ContentCandidate(
            source="chatgpt",
            author_role="assistant",
            content_type="code",
            text=(
                'sales = pd.read_csv("sales.csv")\n'
                'active = sales[sales["status"] == "active"]'
            ),
        )
    )

    assert result.should_explain is True
    assert result.confidence >= 0.90
    assert "pd.read_csv" in result.code


def test_fenced_ai_code_is_detected():
    result = detector.detect(
        ContentCandidate(
            source="claude",
            author_role="assistant",
            text=(
                "Puedes hacerlo así:\n\n"
                "```python\n"
                "for item in items:\n"
                "    print(item)\n"
                "```"
            ),
        )
    )

    assert result.should_explain is True
    assert "for item in items" in result.code


def test_github_page_is_ignored():
    result = detector.detect(
        ContentCandidate(
            source="github",
            author_role="system",
            content_type="code",
            text="assert total == 10",
        )
    )

    assert result.should_explain is False
    assert result.reason == "untrusted_source"


def test_user_code_is_not_treated_as_ai_generated():
    result = detector.detect(
        ContentCandidate(
            source="chatgpt",
            author_role="user",
            content_type="code",
            text="total = sum(values)",
        )
    )

    assert result.should_explain is False
    assert result.reason == "not_ai_authored"


def test_normal_ai_text_does_not_trigger():
    result = detector.detect(
        ContentCandidate(
            source="chatgpt",
            author_role="assistant",
            text=(
                "La mejor estrategia es dividir "
                "el problema en pasos pequeños."
            ),
        )
    )

    assert result.should_explain is False
    assert result.reason == "no_code_detected"
