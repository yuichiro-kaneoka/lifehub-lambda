"""Simple health-check action."""

from typing import Dict, Any, Tuple

from . import register_action


@register_action("ping")
def handle(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """Return a simple heartbeat response."""

    return 200, {"status": "ok", "message": "pong"}


__all__ = ["handle"]
