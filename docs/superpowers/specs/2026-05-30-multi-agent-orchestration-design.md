# Spec - Multi-Agent Orchestration & Journal Partition System

## Goal Description
Implement an elegant **Main Agent & Sub-Agent Orchestration Protocol** simulated in live chat, and restructure the persistent database `data/chess_journal.json` to use a lightweight partitioned format (**Active Capping + Compaction**) to safeguard the LLM context window against long-term token bloat.

---

## Proposed Changes

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
*   Update the **Pre-Move Calculation Protocol** to run a simulated sequence of specialized Sub-Agents managed by a Main Agent:
    *   `[Sub-Agent: Positional Strategist ♟️]`: Identifies long-term positional advantages, development goals, space, and structures.
    *   `[Sub-Agent: Tactical Calculator ⚔️]`: Generates candidate moves and computes variations.
    *   `[Sub-Agent: Blunder Auditor 🔍]`: Verifies square safety, counts defender ratios, and checks moves against `active_lessons`.
    *   `[Main Agent 👑 (Orchestrator)]`: Synthesizes outputs, validates checklists, writes calculations to the database, and plays the selected move.
*   Update the **Pre-Move Calculation Block Format** to reflect the new Main Agent and Sub-Agent structure.
*   Update the **Post-Game Self-Analysis Protocol** to write new lessons compacted into `active_lessons` (capped at max 5) and fully detailed into `archived_lessons`.

---

### [Component: Journal Database & Tests]

#### [MODIFY] [chess_journal.json](file:///home/latuan/Local_Programming/chess_rocket/data/chess_journal.json)
*   Restructure the database from a single flat `lessons_learned` array to a partitioned structure:
    *   `active_lessons` (compacted format: `id`, `motif`, `preventative_rule`; capped at max 5).
    *   `archived_lessons` (comprehensive historical records).

#### [MODIFY] [test_journal.py](file:///home/latuan/Local_Programming/chess_rocket/tests/test_journal.py)
*   Update the test suite to reflect the new partitioned schema (`active_lessons` and `archived_lessons`) ensuring that schema validation and mock dashboard servers handle the updated data structure correctly.

---

## Verification Plan

### Automated Tests
*   Run the updated unit tests using `uv run pytest` to ensure both the dashboard server integration and schema validations pass successfully.

### Manual Verification
*   Execute pre-move calculation sequences and verify that the formatted simulated multi-agent outputs are correctly written to `data/chess_journal.json` under `current_calculations`.
*   Complete a speedrun game and verify that newly generated lessons are properly pushed to `active_lessons` (compact format) and `archived_lessons` (full metadata format), with `active_lessons` capping correctly at 5 items.
