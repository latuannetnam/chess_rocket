# Spec - Actual Sub-Agent Orchestration Protocol Integration

## Goal Description
Transition the chess speedrun protocol from a **simulated** multi-agent sequence to an **actual** tool-driven multi-agent orchestration pipeline. The Main Agent will literally invoke specialized Sub-Agents sequentially using the `invoke_subagent` tool before making a move, enhancing calculation precision, context isolation, and reasoning quality.

---

## Proposed Changes

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
*   Update the **Pre-Move Calculation Protocol** to specify that the Main Agent must sequentially invoke specialized Sub-Agents using the `invoke_subagent` tool:
    *   **Positional Strategist** (`Role="Positional Strategist"`): Evaluates structural layout, space, and long-term plans.
    *   **Tactical Calculator** (`Role="Tactical Calculator"`): Computes tactical threats, candidate moves, and variations, taking the Positional Strategist's assessment as context.
    *   **Blunder Auditor** (`Role="Blunder Auditor"`): Audits the candidate moves against active lessons and completes the core Safety Checklist.
*   Update the **Pre-Move Calculation Block Format** to document the tool calls and structure the sequential pipeline results.

---

## Verification Plan

### Manual Verification
*   During active play, verify that before every move, the Main Agent correctly calls the `invoke_subagent` tool three times sequentially with the specified `Role` and `Prompt`.
*   Confirm that the resulting outputs are successfully synthesized and written to `current_calculations.independent_analysis` in `data/chess_journal.json`.
*   Ensure that the local dashboard continues to parse and display the new tool-driven pre-move calculations seamlessly.
