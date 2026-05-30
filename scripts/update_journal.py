#!/usr/bin/env python3
import argparse
import json
import os
import sys
import shutil
from datetime import datetime, UTC
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
    all_lessons = data.get("active_lessons", []) + data.get("archived_lessons", [])
    max_num = 0
    for l in all_lessons:
        try:
            num = int(l["id"].split("_")[1])
            if num > max_num:
                max_num = num
        except Exception:
            pass
    next_num = max_num + 1
    lesson_id = f"lesson_{next_num:03d}"

    # 3. Format lessons
    new_active = {
        "id": lesson_id,
        "motif": motif.strip(),
        "preventative_rule": preventative_rule.strip()
    }
    new_archive = {
        "id": lesson_id,
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
