"""Action handler for registering or updating recipe metadata."""

from typing import Dict, Any, Tuple

from . import register_action


@register_action("add_recipe")
def handle(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """Validate the payload and return a stub response for recipe creation."""

    required_fields = ["name", "ingredients", "calories", "date"]
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return 400, {
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing_fields)}",
        }

    recipe_summary = {
        "name": payload["name"],
        "ingredients": payload["ingredients"],
        "calories": payload["calories"],
        "date": payload["date"],
    }

    return 200, {
        "status": "ok",
        "recipe": recipe_summary,
    }


__all__ = ["handle"]
