from uuid import uuid4

from fastapi.testclient import TestClient

from code2plain.api.app import app
from tests.demo_test_helper import demo_credentials
from code2plain.human_skill_memory import (
    human_skill_memory,
)


client = TestClient(app)


CODE = (
    'result = active'
    '.groupby("customer_id")'
    '["amount"].sum()'
)


def _user() -> str:
    return (
        "adaptive-test-"
        + uuid4().hex
    )


def test_new_user_receives_full_guidance():
    user_id = _user()

    _, token = demo_credentials(
        client,
        user_id,
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "code": CODE,
            "user_id": user_id,
            "demo_token": token,
        },
    )

    assert response.status_code == 200

    policies = [
        item["teaching_policy"]
        for item in response.json()["items"]
        if item["teaching_policy"]
    ]

    assert policies

    assert any(
        policy["level"] == "guided"
        for policy in policies
    )

    assert any(
        policy["explanation_depth"]
        == "full"
        for policy in policies
    )


def test_demonstrated_progress_reduces_help():
    user_id = _user()

    _, token = demo_credentials(
        client,
        user_id,
    )

    initial = client.post(
        "/v1/context-block-learn",
        json={
            "code": CODE,
            "user_id": user_id,
            "demo_token": token,
        },
    ).json()

    skill_id = next(
        item["skill_id"]
        for item in initial["items"]
        if item["skill_id"]
    )

    for _ in range(3):
        human_skill_memory.record_answer(
            user_id=user_id,
            skill_id=skill_id,
            correct=True,
        )

    _, token = demo_credentials(
        client,
        user_id,
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "code": CODE,
            "user_id": user_id,
            "demo_token": token,
        },
    )

    assert response.status_code == 200

    matching = next(
        item
        for item in response.json()["items"]
        if item["skill_id"] == skill_id
    )

    policy = matching[
        "teaching_policy"
    ]

    assert policy["level"] == "reduced"

    assert (
        policy["explanation_depth"]
        == "compact"
    )

    assert policy["show_why"] is False


def test_struggling_user_keeps_full_support():
    user_id = _user()

    _, token = demo_credentials(
        client,
        user_id,
    )

    initial = client.post(
        "/v1/context-block-learn",
        json={
            "code": CODE,
            "user_id": user_id,
            "demo_token": token,
        },
    ).json()

    skill_id = next(
        item["skill_id"]
        for item in initial["items"]
        if item["skill_id"]
    )

    human_skill_memory.record_answer(
        user_id=user_id,
        skill_id=skill_id,
        correct=False,
    )

    _, token = demo_credentials(
        client,
        user_id,
    )

    response = client.post(
        "/v1/context-block-learn",
        json={
            "code": CODE,
            "user_id": user_id,
            "demo_token": token,
        },
    )

    matching = next(
        item
        for item in response.json()["items"]
        if item["skill_id"] == skill_id
    )

    policy = matching[
        "teaching_policy"
    ]

    assert (
        policy["level"]
        == "reinforcement"
    )

    assert (
        policy["explanation_depth"]
        == "full"
    )

    assert policy["show_why"] is True


def test_request_without_user_is_blocked():
    response = client.post(
        "/v1/context-block-learn",
        json={
            "code":
                CODE,
        },
    )

    assert response.status_code == 403


