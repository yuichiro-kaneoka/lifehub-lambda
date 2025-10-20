"""Action registry for the Lifehub Lambda orchestration layer."""

from typing import Callable, Dict, Tuple, Any

ActionResponse = Tuple[int, Dict[str, Any]]
ActionHandler = Callable[[Dict[str, Any]], ActionResponse]

ACTION_REGISTRY: Dict[str, ActionHandler] = {}


def register_action(name: str) -> Callable[[ActionHandler], ActionHandler]:
    """Decorator used to register an action handler by name."""

    def decorator(func: ActionHandler) -> ActionHandler:
        ACTION_REGISTRY[name] = func
        return func

    return decorator


# Import actions that should be available.
# Additional actions can be exposed by importing their modules here.
from . import add_recipe  # noqa: E402,F401
from . import ping  # noqa: E402,F401

__all__ = ["ACTION_REGISTRY", "register_action"]
