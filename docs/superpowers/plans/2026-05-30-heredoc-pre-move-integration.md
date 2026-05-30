# Heredoc Pre-Move Calculations Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify `AGENTS.md` to guide the agent to pass pre-move planning blocks via a shell Heredoc directly to `update_journal.py` stdin.

**Architecture:** We will replace the temporary file creation and cleanup steps in the **Pre-Move Calculation Protocol** of `AGENTS.md` with explicit shell Heredoc guidance.

**Tech Stack:** Markdown / Documentation.

---

### Task 1: Update Pre-Move Calculation Protocol in `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Replace temporary file instructions with Heredoc command format**

Modify `/home/latuan/Local_Programming/chess_rocket/AGENTS.md` starting at line 58. Replace the old file-handling sentences (lines 58 to 60) with the Heredoc execution format.

**Original Content (approx lines 58-60):**
```markdown
Output the structured results in the chat. Write the exact synthesized block to a temporary file `temp_pre_move.txt`, write it to the journal by running:
`uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" < temp_pre_move.txt`
And delete `temp_pre_move.txt` once the write completes successfully.
```

**New Replacement Content:**
```markdown
Output the structured results in the chat. Write the exact synthesized block to the journal by running the update command with a shell Heredoc (replacing `<game_id>`, `<move>`, and the block body content accordingly):

```bash
uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" << 'EOF'
[Insert exact synthesized block here]
EOF
```
```

- [ ] **Step 2: Commit the documentation changes to git**

Run:
```bash
git add AGENTS.md
git commit -m "docs: use shell Heredoc instead of temporary file for pre-move calculations"
```
