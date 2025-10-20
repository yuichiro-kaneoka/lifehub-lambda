"""Action handler integrating Google Sheets operations."""

from __future__ import annotations

from typing import Any, Dict, Tuple

try:  # pragma: no cover - optional dependency for runtime integration
    from gspread.exceptions import APIError
except ImportError:  # pragma: no cover - fallback during local testing

    class APIError(Exception):
        """Fallback APIError when gspread is unavailable."""

        pass

from . import register_action

try:  # pragma: no cover - provided in deployment environment
    from .gs_client import get_gs_client
except ImportError:  # pragma: no cover - fallback for local testing

    def get_gs_client() -> Any:  # type: ignore[override]
        """Placeholder client loader that should be overridden in production."""

        raise RuntimeError("get_gs_client is not configured")


ActionResponse = Tuple[int, Dict[str, Any]]


@register_action("sync_sheets")
def handle(payload: Dict[str, Any]) -> ActionResponse:
    """Perform append, update, or read operations against Google Sheets."""

    try:
        gc = get_gs_client()
        sheet_id = payload["sheet_id"]
        worksheet_name = payload.get("worksheet", "")
        spreadsheet = gc.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name) if worksheet_name else spreadsheet.sheet1

        mode = payload.get("mode", "append")

        if mode == "append":
            worksheet.append_rows(payload["values"])  # type: ignore[arg-type]
            return 200, {"status": "ok", "operation": "append"}

        if mode == "update":
            worksheet.update(payload["range"], payload["values"])
            return 200, {"status": "ok", "operation": "update"}

        if mode == "read":
            data = worksheet.get(payload["range"])
            return 200, {"status": "ok", "operation": "read", "data": data}

        return 400, {"status": "error", "message": f"Unknown mode: {mode}"}

    except (KeyError, APIError, ValueError) as exc:
        return 400, {"status": "error", "message": str(exc)}


__all__ = ["handle"]
