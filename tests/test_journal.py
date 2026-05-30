"""Pytest tests for Chess Journal persistence and Dashboard Server integration.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.dashboard_server import DashboardHandler

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_ROOT / "data"
_JOURNAL_PATH = _DATA_DIR / "chess_journal.json"


@pytest.fixture()
def temp_journal_cleaner():
    """Backup the chess_journal.json if it exists and restore it after."""
    orig_content = None
    if _JOURNAL_PATH.exists():
        orig_content = _JOURNAL_PATH.read_text(encoding="utf-8")
    
    yield

    if orig_content is not None:
        _JOURNAL_PATH.write_text(orig_content, encoding="utf-8")
    elif _JOURNAL_PATH.exists():
        _JOURNAL_PATH.unlink()


def test_journal_schema_structure(temp_journal_cleaner):
    """Verify that chess_journal.json is in valid JSON format and has the required schema."""
    # Write a test journal
    test_data = {
        "total_games_played": 1,
        "current_learning_elo": 1000,
        "lessons_learned": [
            {
                "id": "lesson_001",
                "timestamp": "2026-05-30T10:15:30Z",
                "game_id": "test_game_123",
                "elo_encountered": 1000,
                "motif": "Open File Danger",
                "concept": "Hanging Queens to Active Rooks",
                "mistake_description": "Captured a pawn blindly.",
                "preventative_rule": "Look before you leap."
            }
        ],
        "current_calculations": {
            "current_game_id": "test_game_123",
            "last_move_played": "e4",
            "independent_analysis": "White plays e4, fighting for center.",
            "pre_move_checklist_passed": True
        }
    }
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _JOURNAL_PATH.write_text(json.dumps(test_data, indent=2), encoding="utf-8")

    # Read and parse
    read_data = json.loads(_JOURNAL_PATH.read_text(encoding="utf-8"))
    assert read_data["total_games_played"] == 1
    assert len(read_data["lessons_learned"]) == 1
    assert read_data["current_calculations"]["pre_move_checklist_passed"] is True
    assert read_data["current_calculations"]["last_move_played"] == "e4"


def test_dashboard_handler_api_journal(temp_journal_cleaner):
    """Test that the DashboardHandler serves the journal correctly via /api/journal."""
    test_data = {
        "total_games_played": 2,
        "current_learning_elo": 1200,
        "lessons_learned": [],
        "current_calculations": {
            "current_game_id": None,
            "last_move_played": None,
            "independent_analysis": "Initial state",
            "pre_move_checklist_passed": False
        }
    }
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _JOURNAL_PATH.write_text(json.dumps(test_data), encoding="utf-8")

    # Instantiate the handler without calling __init__ to avoid socket/parsing logic
    handler = DashboardHandler.__new__(DashboardHandler)
    
    # Mock all HTTP response methods
    handler.send_response = MagicMock()
    handler.send_header = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()

    # Route request to /api/journal
    handler.path = "/api/journal"
    handler.do_GET()

    # Verify send_response(200) was called
    handler.send_response.assert_called_with(200)
    
    # Verify the correct payload was written to wfile
    written_bytes = b"".join(call.args[0] for call in handler.wfile.write.call_args_list)
    written_json = json.loads(written_bytes.decode("utf-8"))
    
    assert written_json["total_games_played"] == 2
    assert written_json["current_learning_elo"] == 1200

