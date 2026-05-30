import json
import os
import sys
from pathlib import Path
import pytest
from unittest.mock import patch

# Programmatic imports from update_journal.
# Note: we add scripts to python path if needed, but pytest runs with scripts in path.
import scripts.update_journal as uj

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_JOURNAL_PATH = _PROJECT_ROOT / "data" / "chess_journal.json"
_BACKUP_PATH = _PROJECT_ROOT / "data" / "chess_journal.json.bak"

@pytest.fixture()
def temp_journal():
    """Backup original journal and restore it after test."""
    orig_content = None
    if _JOURNAL_PATH.exists():
        orig_content = _JOURNAL_PATH.read_text(encoding="utf-8")
    
    yield

    if orig_content is not None:
        _JOURNAL_PATH.write_text(orig_content, encoding="utf-8")
    elif _JOURNAL_PATH.exists():
        _JOURNAL_PATH.unlink()
    if _BACKUP_PATH.exists():
        _BACKUP_PATH.unlink()

def test_print_lessons(temp_journal, capsys):
    """Verify that print-lessons prints the active lessons."""
    test_data = {
        "total_games_played": 1,
        "current_learning_elo": 2000,
        "active_lessons": [
            {
                "id": "lesson_001",
                "motif": "Tactical Motif",
                "preventative_rule": "Test preventative rule."
            }
        ],
        "archived_lessons": [],
        "current_calculations": {
            "current_game_id": None,
            "last_move_played": None,
            "independent_analysis": "Initial state",
            "pre_move_checklist_passed": False
        }
    }
    _JOURNAL_PATH.write_text(json.dumps(test_data, indent=2), encoding="utf-8")

    # Run print_lessons
    uj.print_lessons()

    captured = capsys.readouterr()
    assert "lesson_001" in captured.out
    assert "Tactical Motif" in captured.out
    assert "Test preventative rule." in captured.out

def test_pre_move(temp_journal):
    """Verify pre-move updates current_calculations correctly."""
    test_data = {
        "total_games_played": 1,
        "current_learning_elo": 2000,
        "active_lessons": [],
        "archived_lessons": [],
        "current_calculations": {
            "current_game_id": None,
            "last_move_played": None,
            "independent_analysis": "",
            "pre_move_checklist_passed": False
        }
    }
    _JOURNAL_PATH.write_text(json.dumps(test_data, indent=2), encoding="utf-8")

    analysis_content = "### Pre-Move Analysis\n* Test content."
    
    uj.update_pre_move("test_game_123", "Qb3", analysis_content)

    updated = json.loads(_JOURNAL_PATH.read_text(encoding="utf-8"))
    calc = updated["current_calculations"]
    assert calc["current_game_id"] == "test_game_123"
    assert calc["last_move_played"] == "Qb3"
    assert calc["independent_analysis"] == analysis_content
    assert calc["pre_move_checklist_passed"] is True

def test_post_game_capping(temp_journal):
    """Verify post-game lesson addition and capping at 5 active lessons."""
    test_data = {
        "total_games_played": 1,
        "current_learning_elo": 1000,
        "active_lessons": [
            {"id": f"lesson_00{i}", "motif": f"M_{i}", "preventative_rule": f"R_{i}"} for i in range(1, 6)
        ],
        "archived_lessons": [],
        "current_calculations": {
            "current_game_id": "test_game_123",
            "last_move_played": "Qb3",
            "independent_analysis": "Calculations",
            "pre_move_checklist_passed": True
        }
    }
    _JOURNAL_PATH.write_text(json.dumps(test_data, indent=2), encoding="utf-8")

    mistake_desc = "Made a huge mistake here."
    uj.update_post_game(
        game_id="test_game_123",
        elo=2000,
        motif="New Motif",
        concept="New Concept",
        preventative_rule="New rule to live by.",
        mistake_description=mistake_desc
    )

    updated = json.loads(_JOURNAL_PATH.read_text(encoding="utf-8"))
    
    # Check general counters
    assert updated["total_games_played"] == 2
    assert updated["current_learning_elo"] == 2000

    # Check active lessons capped at 5
    assert len(updated["active_lessons"]) == 5
    # The oldest (lesson_001) should be popped, and new one added at the end (lesson_006)
    active_ids = [l["id"] for l in updated["active_lessons"]]
    assert "lesson_001" not in active_ids
    assert "lesson_006" in active_ids

    # Check archived lessons has the new one
    assert len(updated["archived_lessons"]) == 1
    new_archive = updated["archived_lessons"][0]
    assert new_archive["id"] == "lesson_006"
    assert new_archive["mistake_description"] == mistake_desc
    assert new_archive["preventative_rule"] == "New rule to live by."

    # Verify current_calculations is reset
    calc = updated["current_calculations"]
    assert calc["current_game_id"] is None
    assert calc["last_move_played"] is None
    assert calc["pre_move_checklist_passed"] is False
    assert calc["independent_analysis"] == "Initial state: Waiting for first move."
