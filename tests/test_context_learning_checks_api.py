from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_context_block_returns_evaluable_check():
    response = client.post(
        "/v1/context-block-learn",
        json={
            "code": (
                'result = active'
                '.groupby("customer_id")'
                '["amount"].sum()'
            )
        },
    )

    assert response.status_code == 200

    item = response.json()["items"][0]

    check = item["check"]

    assert check["question"]
    assert len(check["options"]) == 3

    assert "correct_index" not in check
    assert "explanation" not in check


def test_context_csv_check_has_expected_answer():
    response = client.post(
        "/v1/context-block-learn",
        json={
            "code":
                'sales = '
                'pd.read_csv("sales.csv")'
        },
    )

    item = response.json()["items"][0]

    check = item["check"]

    assert "correct_index" not in check

    assert any(
        "nuevo archivo" in option
        for option in check["options"]
    )
