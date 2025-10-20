"""Tests for the sync_sheets action handler."""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from actions.sync_sheets import handle


class DummyWorksheet:
    """Minimal worksheet stub for validating interactions."""

    def __init__(self) -> None:
        self.appended: List[List[Any]] = []
        self.updated: Dict[str, List[List[Any]]] = {}
        self.ranges: Dict[str, List[List[Any]]] = {}

    def append_rows(self, values: List[List[Any]]) -> None:
        self.appended.extend(values)

    def update(self, range_: str, values: List[List[Any]]) -> None:
        self.updated[range_] = values

    def get(self, range_: str) -> List[List[Any]]:
        return self.ranges.get(range_, [])


class DummySpreadsheet:
    """Spreadsheet stub exposing sheet resolution helpers."""

    def __init__(self, worksheet: DummyWorksheet) -> None:
        self.sheet1 = worksheet
        self._worksheet = worksheet

    def worksheet(self, name: str) -> DummyWorksheet:  # pragma: no cover - parity with gspread
        return self._worksheet


class DummyClient:
    """Google Sheets client stub returning a configured spreadsheet."""

    def __init__(self, spreadsheet: DummySpreadsheet) -> None:
        self._spreadsheet = spreadsheet

    def open_by_key(self, sheet_id: str) -> DummySpreadsheet:
        return self._spreadsheet


@pytest.fixture
def worksheet() -> DummyWorksheet:
    return DummyWorksheet()


@pytest.fixture
def monkeypatched_client(monkeypatch: pytest.MonkeyPatch, worksheet: DummyWorksheet) -> None:
    spreadsheet = DummySpreadsheet(worksheet)
    client = DummyClient(spreadsheet)
    monkeypatch.setattr("actions.sync_sheets.get_gs_client", lambda: client)


def test_append_mode(monkeypatched_client: None, worksheet: DummyWorksheet) -> None:
    payload = {
        "action": "sync_sheets",
        "sheet_id": "sheet",
        "values": [["a", "b"]],
    }

    status, body = handle(payload)

    assert status == 200
    assert body == {"status": "ok", "operation": "append"}
    assert worksheet.appended == [["a", "b"]]


def test_update_mode(monkeypatched_client: None, worksheet: DummyWorksheet) -> None:
    payload = {
        "action": "sync_sheets",
        "sheet_id": "sheet",
        "mode": "update",
        "range": "A1:B2",
        "values": [[1, 2], [3, 4]],
    }

    status, body = handle(payload)

    assert status == 200
    assert body == {"status": "ok", "operation": "update"}
    assert worksheet.updated["A1:B2"] == [[1, 2], [3, 4]]


def test_read_mode(monkeypatched_client: None, worksheet: DummyWorksheet) -> None:
    worksheet.ranges["A1:B2"] = [["v1", "v2"]]
    payload = {
        "action": "sync_sheets",
        "sheet_id": "sheet",
        "mode": "read",
        "range": "A1:B2",
    }

    status, body = handle(payload)

    assert status == 200
    assert body == {
        "status": "ok",
        "operation": "read",
        "data": [["v1", "v2"]],
    }


def test_unknown_mode(monkeypatched_client: None) -> None:
    payload = {
        "action": "sync_sheets",
        "sheet_id": "sheet",
        "mode": "delete",
    }

    status, body = handle(payload)

    assert status == 400
    assert body == {"status": "error", "message": "Unknown mode: delete"}


def test_missing_required_field(monkeypatched_client: None) -> None:
    payload = {"action": "sync_sheets", "mode": "append"}

    status, body = handle(payload)

    assert status == 400
    assert body["status"] == "error"


def test_value_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_value_error() -> Any:
        raise ValueError("bad data")

    monkeypatch.setattr("actions.sync_sheets.get_gs_client", raise_value_error)

    payload = {"action": "sync_sheets", "sheet_id": "sheet"}

    status, body = handle(payload)

    assert status == 400
    assert body == {"status": "error", "message": "bad data"}
