# Spec - Shell Heredoc Pre-Move Calculations Integration

## Goal Description
To simplify the pre-move calculations execution and avoid creating and deleting physical files (like `temp_pre_move.txt`) for each move, we will update the pre-move protocol in `AGENTS.md` to use a standard shell Heredoc (`<< 'EOF' ... EOF`). This pipes the planning block directly to `scripts/update_journal.py` stdin from the terminal.

---

## Proposed Changes

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
*   Replace the temporary file instructions (lines 58 to 60) with clear Heredoc execution instructions.

---

## Verification Plan

### Manual Verification
*   Execute a pre-move calculation using the new Heredoc instruction format.
*   Verify that the data is successfully written to `data/chess_journal.json`'s `current_calculations.independent_analysis` field without any file created or cleaned up.
