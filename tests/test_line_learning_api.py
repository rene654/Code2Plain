from fastapi.testclient import TestClient

from code2plain.api.app import app


client = TestClient(app)


def test_line_by_line_api():
    response = client.post(
        "/v1/line-by-line",
        json={
            "code": (
                'sales = pd.read_csv("sales.csv")\n'
                'active = sales['
                'sales["status"] == "active"]\n'
                'result = active.groupby("customer")'
                '["amount"].sum()'
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["explained_lines"] >= 3
    assert payload["items"]
