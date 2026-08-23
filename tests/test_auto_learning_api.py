from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_chatgpt_new_code_returns_microlearning():
    response = client.post(
        "/v1/auto-learn",
        json={
            "source": "chatgpt",
            "author_role": "assistant",
            "content_type": "code",
            "text": (
                'fresh_data_881 = sales['
                'sales["status"] == "active"]\n'
                'fresh_group_881 = '
                'fresh_data_881.groupby("customer")'
            ),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["should_teach"] is True
    assert len(payload["items"]) <= 3

    concepts = [
        item["concept"]
        for item in payload["items"]
    ]

    assert "FILTER" in concepts
    assert "GROUP" in concepts


def test_non_ai_source_stays_silent():
    response = client.post(
        "/v1/auto-learn",
        json={
            "source": "documentation",
            "author_role": "system",
            "content_type": "code",
            "text": (
                "for doc_item_991 in docs:\n"
                "    print(doc_item_991)"
            ),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["should_teach"] is False


def test_same_ai_code_does_not_repeat():
    payload = {
        "source": "chatgpt",
        "author_role": "assistant",
        "content_type": "code",
        "text": (
            "for unique_item_771 in unique_items_771:\n"
            "    print(unique_item_771)"
        ),
    }

    first = client.post(
        "/v1/auto-learn",
        json=payload,
    ).json()

    second = client.post(
        "/v1/auto-learn",
        json=payload,
    ).json()

    assert first["should_teach"] is True
    assert second["should_teach"] is False
