import json
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import lambda_handler


def build_event(path="/task", method="POST", body=None):
    event = {
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
            }
        }
    }
    if body is not None:
        event["body"] = json.dumps(body)
    return event


def test_task_add_recipe_success():
    event = build_event(
        body={
            "action": "add_recipe",
            "name": "Test Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "calories": 500,
            "date": "2025-10-20",
        }
    )

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["status"] == "ok"
    assert body["recipe"]["name"] == "Test Recipe"


def test_task_missing_action():
    event = build_event(body={"name": "Test"})

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["status"] == "error"
    assert "action" in body["message"]


def test_task_unknown_action():
    event = build_event(body={"action": "nonexistent"})

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["status"] == "error"
    assert "Unknown action" in body["message"]


def test_task_invalid_json():
    event = build_event()
    event["body"] = "invalid json"

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["status"] == "error"


def test_task_not_found_path():
    event = build_event(path="/other")

    response = lambda_handler(event, {})

    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert body["status"] == "error"
