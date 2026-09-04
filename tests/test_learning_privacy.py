import pytest

from code2plain.privacy import (
    LearningPrivacyBoundary,
)


def test_learning_memory_accepts_abstract_concept():
    privacy = LearningPrivacyBoundary()

    assert (
        privacy.validate_concept(
            "FUNCTION_CALL"
        )
        == "FUNCTION_CALL"
    )


def test_learning_memory_rejects_multiline_code():
    privacy = LearningPrivacyBoundary()

    with pytest.raises(ValueError):
        privacy.validate_concept(
            'result = model.predict(data)\n'
            'print(result)'
        )


def test_persistent_payload_rejects_code():
    privacy = LearningPrivacyBoundary()

    with pytest.raises(ValueError):
        privacy.validate_payload(
            {
                "concept": "FUNCTION_CALL",
                "code":
                    "TOP_SECRET_CLIENT_"
                    "ALGORITHM_X9281",
            }
        )


def test_persistent_payload_rejects_source_text():
    privacy = LearningPrivacyBoundary()

    with pytest.raises(ValueError):
        privacy.validate_payload(
            {
                "concept": "FILTERING",
                "source_code":
                    "CONFIDENTIAL_SOURCE",
            }
        )


def test_learning_payload_allows_progress_only():
    privacy = LearningPrivacyBoundary()

    privacy.validate_payload(
        {
            "concept": "FUNCTION_CALL",
            "seen": 4,
            "correct": 2,
            "incorrect": 2,
        }
    )
