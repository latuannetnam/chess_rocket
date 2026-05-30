# Tool-Driven Sub-Agent Orchestration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transition the pre-move protocol in `AGENTS.md` from a simulated sequence to an actual sequential `invoke_subagent` tool pipeline.

**Architecture:** We will modify the **Pre-Move Calculation Protocol** and the **Pre-Move Calculation Block Format** sections inside `AGENTS.md` to define explicit parameters for each sub-agent's role, prompt template, and tool call structure.

**Tech Stack:** Markdown / Guidelines text.

---

### Task 1: Update Pre-Move Protocols in `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Replace simulated pre-move text in `AGENTS.md` with explicit tool-based `invoke_subagent` specifications**

Update the Pre-Move Calculation Protocol section (lines 44 to 78) in `AGENTS.md` to specify:
1. Sequential invocation of `invoke_subagent` for each specialized role.
2. The concrete schema and properties (Role, Prompt, context inheritance).
3. The exact structured formatting for the pre-move calculation blocks written to the database.

Apply the following modifications to `AGENTS.md`:

```diff
- ### 2. Pre-Move Calculation Protocol
- Before playing any move using the `make_move` tool:
- 1. Run a simulated multi-agent sequential analysis involving specialized Sub-Agents managed by the Main Agent.
- 2. Output a structured multi-agent coordination block in the chat in the format below.
- 3. Write the exact analysis block to `current_calculations.independent_analysis` in `data/chess_journal.json`, and set `current_calculations.pre_move_checklist_passed` to `true` (once all checks are done), `current_calculations.current_game_id` to the active `game_id`, and `current_calculations.last_move_played` to your selected move.
- 
- **Pre-Move Calculation Block Format:**
- ```markdown
- ### 👑 Main Agent: Move X Planning
- *   **Active Lessons Loaded**: [List all active lesson IDs from active_lessons]
- 
- #### ♟️ [Sub-Agent: Positional Strategist]
- *   **Positional Assessment**: [Evaluate long-term structures, space advantages, king safety, and plans]
- *   **Key Squares/Targets**: [List vital squares or pieces to target or defend]
- 
- #### ⚔️ [Sub-Agent: Tactical Calculator]
- *   **Opponent's Threats**: [Analyze what Stockfish's last move threatens]
- *   **Candidate Moves**:
-     1. [Move A] - *Line*: [A -> B -> C] - *Pros/Cons*: [Quick assessment]
-     2. [Move B] - *Line*: [X -> Y -> Z] - *Pros/Cons*: [Quick assessment]
- 
- #### 🔍 [Sub-Agent: Blunder Auditor]
- *   **Audit against Active Lessons**:
-     - [Move A] -> [Blunder Audit vs active_lessons (e.g., Safe from forks? Yes. Defended? Yes.)]
-     - [Move B] -> [Blunder Audit vs active_lessons]
- *   **Safety Checklist**:
-     - [x] Stored lessons blunder audit passed for the selected move.
-     - [x] Target square is safe and not attacked by hidden long-range pieces.
-     - [x] No hanging major pieces.
-     - [x] King safety / back-rank checkmate threats assessed.
- 
- #### 👑 [Main Agent: Final Synthesis]
- *   **Decision**: Play [Selected Move]
- ```
+ ### 2. Pre-Move Calculation Protocol
+ Before playing any move using the `make_move` tool, the **Main Agent** must sequentially invoke three specialized sub-agents using the `invoke_subagent` tool:
+ 
+ 1. **Positional Strategist**:
+    - **Tool Call**: `invoke_subagent(Role="Positional Strategist", Prompt="Evaluate the current chess position. Focus on long-term structures, space advantages, king safety, and plans. Identify key squares or pieces to target or defend. Current FEN: [Insert Board FEN]")`
+ 2. **Tactical Calculator**:
+    - **Tool Call**: `invoke_subagent(Role="Tactical Calculator", Prompt="Identify opponent threats and calculate candidate moves. Consider this positional context: [Insert Positional Strategist Output]. Current FEN: [Insert Board FEN]")`
+ 3. **Blunder Auditor**:
+    - **Tool Call**: `invoke_subagent(Role="Blunder Auditor", Prompt="Audit the candidate moves: [Insert Tactical Calculator Output] against the active lessons: [Insert active_lessons]. Complete the Safety Checklist. Current FEN: [Insert Board FEN]")`
+ 
+ Output the structured results in the chat and write the exact synthesized block to `current_calculations.independent_analysis` in `data/chess_journal.json`. Set `current_calculations.pre_move_checklist_passed` to `true`, `current_calculations.current_game_id` to the active `game_id`, and `current_calculations.last_move_played` to your selected move.
+ 
+ **Pre-Move Calculation Block Format:**
+ ```markdown
+ ### 👑 Main Agent: Move X Planning
+ *   **Active Lessons Loaded**: [List all active lesson IDs from active_lessons]
+ 
+ #### ♟️ [Sub-Agent: Positional Strategist] - Tool Call: `invoke_subagent(Role="Positional Strategist", ...)`
+ *   **Positional Assessment**: [Direct output from the Positional Strategist sub-agent]
+ 
+ #### ⚔️ [Sub-Agent: Tactical Calculator] - Tool Call: `invoke_subagent(Role="Tactical Calculator", ...)`
+ *   **Opponent's Threats**: [Direct threat assessment from the Tactical Calculator sub-agent]
+ *   **Candidate Moves**:
+     1. [Move A] - *Line*: [A -> B -> C] - *Pros/Cons*: [Calculation from sub-agent]
+     2. [Move B] - *Line*: [X -> Y -> Z] - *Pros/Cons*: [Calculation from sub-agent]
+ 
+ #### 🔍 [Sub-Agent: Blunder Auditor] - Tool Call: `invoke_subagent(Role="Blunder Auditor", ...)`
+ *   **Audit against Active Lessons**:
+     - [Move A] -> [Blunder Audit vs active_lessons (e.g., Safe from forks? Yes. Defended? Yes.)]
+     - [Move B] -> [Blunder Audit vs active_lessons]
+ *   **Safety Checklist**:
+     - [x] Stored lessons blunder audit passed for the selected move.
+     - [x] Target square is safe and not attacked by hidden long-range pieces.
+     - [x] No hanging major pieces.
+     - [x] King safety / back-rank checkmate threats assessed.
+ 
+ #### 👑 [Main Agent: Final Synthesis]
+ *   **Decision**: Play [Selected Move]
+ ```
```

- [ ] **Step 2: Commit the changes to git**

Run:
```bash
git add AGENTS.md
git commit -m "feat: implement actual sub-agent orchestration pipeline in AGENTS.md"
```
