# Automated Journal Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a robust Python database management CLI utility `scripts/update_journal.py` to handle all persistent reading and writing operations to `data/chess_journal.json`, preventing JSON formatting bugs and errors.

**Architecture:** A single unified script encapsulating atomic backup-and-write capabilities, input validation, and cap-checking. The LLM agent's workflow in `AGENTS.md` is updated to replace manual file replacements with reliable CLI subcommands.

**Tech Stack:** Python 3.12 (Standard Library modules only: `json`, `argparse`, `datetime`, `os`, `sys`, `shutil`, `pathlib`).

---

### Task 1: Create Test Suite for Journal Utility

**Files:**
- Create: `tests/test_update_journal.py`
- Test: `tests/test_update_journal.py`

- [ ] **Step 1: Write unit tests for update_journal.py**

Create `tests/test_update_journal.py` with the following comprehensive tests verifying each subcommand:
```python
import json
import os
import sys
from pathlib import Path
import pytest
from unittest.mock import patch

# Mock standard system execution or import our script functions if needed.
# Since the script runs as a CLI, we can test its programmatic operations by importing it or running via sys.argv.
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
```

- [ ] **Step 2: Commit initial test shell**

```bash
git add tests/test_update_journal.py
git commit -m "test: add test suite for automated journal management"
```

---

### Task 2: Implement Automated Journal Utility Script

**Files:**
- Create: `scripts/update_journal.py`
- Test: `tests/test_update_journal.py`

- [ ] **Step 1: Write programmatic utility functions**

Create `scripts/update_journal.py` containing programmatic helper functions for database actions and strict error-handling backup logic:
```python
#!/usr/bin/env python3
import argparse
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_JOURNAL_PATH = _PROJECT_ROOT / "data" / "chess_journal.json"
_BACKUP_PATH = _PROJECT_ROOT / "data" / "chess_journal.json.bak"

def _load_journal() -> dict:
    if not _JOURNAL_PATH.exists():
        sys.exit(f"Error: Journal file {_JOURNAL_PATH} not found.")
    try:
        with open(_JOURNAL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Malformed JSON in journal: {e}")

def _save_journal_safely(data: dict):
    # Ensure backup directory exists
    _JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Create a backup of the current state
    if _JOURNAL_PATH.exists():
        shutil.copy2(_JOURNAL_PATH, _BACKUP_PATH)
    
    try:
        # 2. Write the new JSON
        with open(_JOURNAL_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 3. Read back and verify validity
        with open(_JOURNAL_PATH, "r", encoding="utf-8") as f:
            json.load(f)
            
    except Exception as e:
        # 4. If invalid, restore backup
        if _BACKUP_PATH.exists():
            shutil.copy2(_BACKUP_PATH, _JOURNAL_PATH)
        sys.exit(f"Error during save. File restored. Exception: {e}")
    finally:
        # Clean up backup
        if _BACKUP_PATH.exists():
            os.remove(_BACKUP_PATH)

def print_lessons():
    data = _load_journal()
    lessons = data.get("active_lessons", [])
    if not lessons:
        print("No active lessons found.")
        return
    
    print("\n==================================================")
    print("📚 ACTIVE CHESS LESSONS (BLUNDER PREVENTION)")
    print("==================================================")
    for l in lessons:
        print(f"\nID  : {l['id']}")
        print(f"Motif: {l['motif']}")
        print(f"Rule : {l['preventative_rule']}")
    print("\n==================================================")

def update_pre_move(game_id: str, move: str, analysis: str):
    data = _load_journal()
    data["current_calculations"] = {
        "current_game_id": game_id,
        "last_move_played": move,
        "independent_analysis": analysis.strip(),
        "pre_move_checklist_passed": True
    }
    _save_journal_safely(data)
    print(f"Successfully saved pre-move calculations for {move}.")

def update_post_game(game_id: str, elo: int, motif: str, concept: str, preventative_rule: str, mistake_description: str):
    data = _load_journal()
    
    # 1. Update general stats
    data["total_games_played"] = data.get("total_games_played", 0) + 1
    data["current_learning_elo"] = elo

    # 2. Compute next lesson ID
    archived = data.get("archived_lessons", [])
    next_num = len(archived) + 1
    lesson_id = f"lesson_{next_num:03d}"

    # 3. Format lessons
    new_active = {
        "id": lesson_id,
        "motif": motif.strip(),
        "preventative_rule": preventative_rule.strip()
    }
    new_archive = {
        "id": lesson_id,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "game_id": game_id,
        "elo_encountered": elo,
        "motif": motif.strip(),
        "concept": concept.strip(),
        "mistake_description": mistake_description.strip(),
        "preventative_rule": preventative_rule.strip()
    }

    # 4. Append
    if "active_lessons" not in data:
        data["active_lessons"] = []
    if "archived_lessons" not in data:
        data["archived_lessons"] = []
        
    data["active_lessons"].append(new_active)
    data["archived_lessons"].append(new_archive)

    # 5. Cap active lessons list at exactly 5
    if len(data["active_lessons"]) > 5:
        data["active_lessons"] = data["active_lessons"][-5:]

    # 6. Reset calculations
    data["current_calculations"] = {
        "current_game_id": None,
        "last_move_played": None,
        "independent_analysis": "Initial state: Waiting for first move.",
        "pre_move_checklist_passed": False
    }

    _save_journal_safely(data)
    print(f"Successfully recorded post-game analysis and registered {lesson_id}.")

def main():
    parser = argparse.ArgumentParser(description="Reliable Chess Journal Management CLI")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # print-lessons
    subparsers.add_parser("print-lessons")

    # pre-move
    pre_parser = subparsers.add_parser("pre-move")
    pre_parser.add_argument("--game-id", required=True, help="Active Game ID")
    pre_parser.add_argument("--move", required=True, help="SAN Move played")

    # post-game
    post_parser = subparsers.add_parser("post-game")
    post_parser.add_argument("--game-id", required=True, help="Finished Game ID")
    post_parser.add_argument("--elo", type=int, required=True, help="Elo Rating of opponent")
    post_parser.add_argument("--motif", required=True, help="Blunder Motif")
    post_parser.add_argument("--concept", required=True, help="Chess tactical concept")
    post_parser.add_argument("--rule", required=True, help="Preventative Rule formulation")

    args = parser.parse_args()

    if args.action == "print-lessons":
        print_lessons()
    elif args.action == "pre-move":
        # Read large analysis block from stdin
        analysis = sys.stdin.read()
        update_pre_move(args.game_id, args.move, analysis)
    elif args.action == "post-game":
        # Read mistake description from stdin
        mistake = sys.stdin.read()
        update_post_game(args.game_id, args.elo, args.motif, args.concept, args.rule, mistake)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable and verify existing tests**

Run: `chmod +x scripts/update_journal.py`
Run: `uv run pytest tests/test_update_journal.py -v`
Expected: ALL tests pass successfully.

- [ ] **Step 3: Commit code**

```bash
git add scripts/update_journal.py
git commit -m "feat: implement atomic chess journal management CLI"
```

---

### Task 3: Update Agent Context and Instructions

**Files:**
- Modify: `AGENTS.md`
- Test: Manual validation

- [ ] **Step 1: Replace manual database edits in `AGENTS.md`**

Use code replacement to edit `/home/latuan/Local_Programming/chess_rocket/AGENTS.md`.

Replace lines 38-42 with:
```markdown
### 1. Pre-Game: Load Memory & Lessons
Before calling `new_game` to start a match:
1. Run the print subcommand of our journal tool: `uv run python scripts/update_journal.py print-lessons`
2. Print the exact printed output directly in the chat to maintain context.
3. Keep these preventative rules in active context to avoid repeating past blunders.
```

Replace lines 53-54 with:
```markdown
Output the structured results in the chat. Write the exact synthesized block to a temporary file `temp_pre_move.txt`, write it to the journal by running:
`uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" < temp_pre_move.txt`
And delete `temp_pre_move.txt` once the write completes successfully.
```

Replace lines 89-94 with:
```markdown
4. Update `data/chess_journal.json` safely by running our database utility:
   - Write the mistake description to a temporary file `temp_mistake.txt`.
   - Update the database by running:
     `uv run python scripts/update_journal.py post-game --game-id "<game_id>" --elo <elo> --motif "<motif>" --concept "<concept>" --rule "<preventative_rule>" < temp_mistake.txt`
   - Delete `temp_mistake.txt` once the transaction finishes successfully.
```

- [ ] **Step 2: Commit updated agent guidelines**

```bash
git add AGENTS.md
git commit -m "docs: update agent instructions to use automated journal editing utility"
```

---

### Task 4: Complete Validation and Verification

**Files:**
- Test: Manual verify of print-lessons, pre-move, and post-game actions.

- [ ] **Step 1: Verify `print-lessons`**

Run: `uv run python scripts/update_journal.py print-lessons`
Expected: Beautiful output displaying `lesson_008`, `lesson_009`, `lesson_010`, `lesson_011`, `lesson_012` active lessons.

- [ ] **Step 2: Verify `pre-move`**

Run:
```bash
echo "### Mock Pre-Move calculations" > temp_pre_move.txt
uv run python scripts/update_journal.py pre-move --game-id "test-uuid-123" --move "e4" < temp_pre_move.txt
rm temp_pre_move.txt
```
Expected: Prints `Successfully saved pre-move calculations for e4`. Check `data/chess_journal.json` to verify that `current_calculations` contains the mock block and `pre_move_checklist_passed: true`.

- [ ] **Step 3: Run comprehensive test suites**

Run: `uv run pytest -v`
Expected: ALL test suites pass (both test_journal.py and test_update_journal.py).
