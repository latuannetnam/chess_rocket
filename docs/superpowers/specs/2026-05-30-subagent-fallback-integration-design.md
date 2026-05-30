# Spec - Official Sub-Agent API Signature and Runtime Fallback Protocol

## Goal Description
In some environments (e.g., Gemini CLI), the `invoke_subagent` tool is not physically registered or exposed to the model, leading to execution failures during move calculations. To resolve this:
1. We align our documentation in `AGENTS.md` with the official Google Antigravity subagent API signature by specifying the required parameters: `Role`, `Prompt`, and `TypeName="self"`.
2. We establish a robust **Runtime Fallback Clause** enabling the agent to simulate the three specialized sub-agents sequentially in-line within its own thought process when the physical tool is missing, while outputting the exact same pre-move calculation logs to `data/chess_journal.json`.

---

## Proposed Changes

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
*   Update the **Pre-Move Calculation Protocol** to specify the `invoke_subagent` tool's official parameters (`Role`, `Prompt`, `TypeName="self"`).
*   Add the **Runtime Fallback Clause** enabling seamless simulation in environments where the physical tool is absent.
*   Update the **Pre-Move Calculation Block Format** to document the tool calls/simulation states and structure the sequential pipeline results.

---

## Verification Plan

### Manual Verification
*   During active play, check if the `invoke_subagent` tool is available in our tool declarations.
*   If the tool is missing, verify that the Main Agent adopts the fallback clause, simulates the Positional, Tactical, and Auditor steps sequentially inside the conversation block, and saves the synthesized results cleanly to `data/chess_journal.json`.
*   Ensure that `scripts/update_journal.py` successfully writes the pre-move calculations to the database without errors.
