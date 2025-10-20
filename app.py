"""AWS Lambda entrypoint exposing a task-based orchestration layer."""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from actions import ACTION_REGISTRY, ActionHandler

DEFAULT_HEADERS = {"Content-Type": "application/json"}


class BadRequest(Exception):
    """Raised when the input payload is invalid."""


def build_response(status_code: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return an API Gateway compatible response."""

    return {
        "statusCode": status_code,
        "headers": DEFAULT_HEADERS,
        "body": json.dumps(payload),
    }


def resolve_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and validate the JSON body from the API Gateway event."""

    body = event.get("body")
    if body is None:
        raise BadRequest("No body provided")

    if isinstance(body, str):
        try:
            return json.loads(body or "{}")
        except json.JSONDecodeError as exc:
            raise BadRequest("Invalid JSON") from exc

    if isinstance(body, dict):
        return body

    raise BadRequest("Body must be a JSON string or object")


def dispatch_action(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """Route payload to the appropriate action handler."""

    action_name = payload.get("action")
    if not action_name:
        raise BadRequest("'action' is required")

    handler: ActionHandler | None = ACTION_REGISTRY.get(action_name)
    if handler is None:
        raise BadRequest(f"Unknown action: {action_name}")

    return handler(payload)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:  # noqa: D401
    """AWS Lambda handler that orchestrates task execution based on action."""

    request_context = event.get("requestContext", {}).get("http", {})
    http_method = request_context.get("method", "")
    path = request_context.get("path", "")

    if path != "/task" or http_method.upper() != "POST":
        return build_response(404, {"status": "error", "message": "Not found"})

    try:
        payload = resolve_body(event)
        status_code, result = dispatch_action(payload)
        return build_response(status_code, result)
    except BadRequest as exc:
        return build_response(400, {"status": "error", "message": str(exc)})
    except Exception as exc:  # pragma: no cover - safeguard for unexpected errors
        return build_response(500, {"status": "error", "message": str(exc)})
