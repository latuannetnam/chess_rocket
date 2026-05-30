# Spec - Automated Journal Management & Reliable Edits

## Goal Description
Establish a robust, automated Python command-line utility (`scripts/update_journal.py`) to manage all reading and writing operations to the persistent `data/chess_journal.json` database. This ensures complete reliability of database edits, enforces correct JSON formatting, prevents formatting syntax errors, and simplifies the LLM agent's workflow by removing manual JSON file-replace actions.

---

## Proposed Changes

### [Component: Database Utility Script]

#### [NEW] [update_journal.py](file:///home/latuan/Local_Programming/chess_rocket/scripts/update_journal.py)
A single Python command-line tool that performs atomic updates and pretty-printed reads on the journal file.

*   **Architecture & Operations**:
    *   **Atomic Write & Verification**: Before writing, create a backup copy at `data/chess_journal.json.bak`. Write the new JSON, load it back to verify syntax correctness, and restore from backup if any exception occurs.
    *   **Action `print-lessons`**: Read `data/chess_journal.json`, parse the `active_lessons` list, and print a formatted text summary for direct chat context load.
    *   **Action `pre-move`**: Read `stdin` for the multi-line sub-agent calculations, strip any surrounding whitespace, and write it to `current_calculations.independent_analysis`, setting `pre_move_checklist_passed` to `true`, `last_move_played` to the argument value, and `current_game_id` to the active UUID.
    *   **Action `post-game`**: Read `stdin` for the multi-line mistake description. Compute the UTC timestamp, append a new lesson to both active and archived partitions, enforce a strict cap of 5 on the active lessons list (popping the oldest if it exceeds 5), and reset the `current_calculations` dictionary to its default state.

---

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
Update the game flow protocols to mandate the use of `scripts/update_journal.py` for all reading and writing tasks:

*   **Pre-Game Protocol**:
    *   Run `uv run python scripts/update_journal.py print-lessons` and print the exact stdout summary directly to the chat.
*   **Pre-Move Calculation Protocol**:
    *   Output the structured calculations in the chat.
    *   Write the synthesized pre-move analysis block into a temporary file `temp_pre_move.txt`.
    *   Execute `uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move_played>" < temp_pre_move.txt`.
    *   Delete `temp_pre_move.txt`.
*   **Post-Game Self-Analysis Protocol**:
    *   Perform the analysis and formulate the preventative rule.
    *   Write the mistake description to a temporary file `temp_mistake.txt`.
    *   Execute `uv run python scripts/update_journal.py post-game --game-id "<game_id>" --elo <elo> --motif "<motif>" --concept "<concept>" --rule "<preventative_rule>" < temp_mistake.txt`.
    *   Delete `temp_mistake.txt`.

---

## Verification Plan

### Automated Tests
*   Run the pytest suite to verify no regressions in current journal schema parsing:
    `uv run pytest tests/test_journal.py`

### Manual Verification
1.  **Print Lessons**: Verify that `uv run python scripts/update_journal.py print-lessons` correctly outputs the active capped list.
2.  **Pre-Move Update**:
    *   Write a mock markdown block to a temporary file.
    *   Run the `pre-move` command.
    *   Verify `data/chess_journal.json` is updated and remains 100% valid JSON.
3.  **Post-Game Lesson Addition & Capping**:
    *   Write a mock mistake description to a temporary file.
    *   Run the `post-game` command.
    *   Verify the lesson is appended, active lessons are capped at 5, and calculations are reset.
