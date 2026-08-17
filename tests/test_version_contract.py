from fastapi.testclient import TestClient

from code2plain.api.app import app
from code2plain.version import __version__


def test_code2plain_version_is_v1_1_0():

    assert __version__ == "1.1.0"


def test_fastapi_version_matches_product_version():

    assert app.version == __version__


def test_health_version_matches_product_version():

    client = TestClient(
        app
    )

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "version"
        ]
        == __version__
    )
