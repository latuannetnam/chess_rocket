# Sub-Agent Fallback Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `AGENTS.md` to document the official Google Antigravity subagent tool signature and establish a Runtime Fallback Clause for environments where the physical tool is not registered.

**Architecture:** We will modify the **Pre-Move Calculation Protocol** and the **Pre-Move Calculation Block Format** sections inside `AGENTS.md` to define explicit parameters for each sub-agent's role, prompt template, and tool call structure (adding `TypeName="self"`), while adding a clear in-line simulation fallback clause.

**Tech Stack:** Markdown / Documentation.

---

### Task 1: Update Pre-Move Calculation Protocol in `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Edit `AGENTS.md` to add the official parameters and Runtime Fallback Clause**

Modify `/home/latuan/Local_Programming/chess_rocket/AGENTS.md` starting at line 44. Replace the old `Pre-Move Calculation Protocol` section (lines 44 to 84) with the new tool-compliant and fallback-enabled structure.

**Original Content (approx lines 44-84):**
```markdown
### 2. Pre-Move Calculation Protocol
Before playing any move using the `make_move` tool, the **Main Agent** must sequentially invoke three specialized sub-agents using the `invoke_subagent` tool:

1. **Positional Strategist**:
   - **Tool Call**: `invoke_subagent(Role="Positional Strategist", Prompt="Evaluate the current chess position. Focus on long-term structures, space advantages, king safety, and plans. Identify key squares or pieces to target or defend. Current FEN: [Insert Board FEN]")`
2. **Tactical Calculator**:
   - **Tool Call**: `invoke_subagent(Role="Tactical Calculator", Prompt="Identify opponent threats and calculate candidate moves. Consider this positional context: [Insert Positional Strategist Output]. Current FEN: [Insert Board FEN]")`
3. **Blunder Auditor**:
   - **Tool Call**: `invoke_subagent(Role="Blunder Auditor", Prompt="Audit the candidate moves: [Insert Tactical Calculator Output] against the active lessons: [Insert active_lessons]. Complete the Safety Checklist. Current FEN: [Insert Board FEN]")`

Output the structured results in the chat. Write the exact synthesized block to a temporary file `temp_pre_move.txt`, write it to the journal by running:
`uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" < temp_pre_move.txt`
And delete `temp_pre_move.txt` once the write completes successfully.

**Pre-Move Calculation Block Format:**
```

**New Replacement Content:**
```markdown
### 2. Pre-Move Calculation Protocol
Before playing any move using the `make_move` tool, the **Main Agent** must sequentially invoke three specialized sub-agents using the `invoke_subagent` tool.

#### ⚠️ Runtime Fallback Clause
If the `invoke_subagent` tool is **not** registered or available in the current environment's toolset (e.g., in some Gemini CLI configurations or custom tool-restricted runtimes), the Main Agent must **simulate** the sub-agents sequentially in-line within its own thought process, adopting each persona and generating their respective outputs. The final Pre-Move Calculation Block format must remain identical in either case.

#### Sub-Agent Execution Pipeline
1. **Positional Strategist**:
   - **Tool Call**: `invoke_subagent(Role="Positional Strategist", Prompt="Evaluate the current chess position. Focus on long-term structures, space advantages, king safety, and plans. Identify key squares or pieces to target or defend. Current FEN: [Insert Board FEN]", TypeName="self")`
2. **Tactical Calculator**:
   - **Tool Call**: `invoke_subagent(Role="Tactical Calculator", Prompt="Identify opponent threats and calculate candidate moves. Consider this positional context: [Insert Positional Strategist Output]. Current FEN: [Insert Board FEN]", TypeName="self")`
3. **Blunder Auditor**:
   - **Tool Call**: `invoke_subagent(Role="Blunder Auditor", Prompt="Audit the candidate moves: [Insert Tactical Calculator Output] against the active lessons: [Insert active_lessons]. Complete the Safety Checklist. Current FEN: [Insert Board FEN]", TypeName="self")`

Output the structured results in the chat. Write the exact synthesized block to a temporary file `temp_pre_move.txt`, write it to the journal by running:
`uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" < temp_pre_move.txt`
And delete `temp_pre_move.txt` once the write completes successfully.

**Pre-Move Calculation Block Format:**
```

- [ ] **Step 2: Commit the documentation changes to git**

Run:
```bash
git add AGENTS.md
git commit -m "docs: integrate official subagent signature and fallback clause in AGENTS.md"
```
