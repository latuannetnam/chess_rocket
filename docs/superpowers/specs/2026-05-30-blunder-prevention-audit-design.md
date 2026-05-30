# Spec - Active Blunder-Prevention Audit System

## Goal Description
Implement an explicit Candidate Move Verification Checklist ("Blunder-Prevention Audit") within the agent's pre-move chess calculation lifecycle. This forces the agent to test-simulate every candidate move against all active database lessons in `data/chess_journal.json` to actively prevent repeating past blunders.

---

## Proposed Changes

### [Component: Agent Instructions]

#### [MODIFY] [AGENTS.md](file:///home/latuan/Local_Programming/chess_rocket/AGENTS.md)
Update the `Pre-Move Calculation Protocol` and the `Pre-Move Calculation Block Format` to incorporate a detailed blunder audit per candidate move.

---

## Verification Plan

### Automated Verification
- Run existing test suites (`uv run pytest`) to ensure all schemas and tests are still fully correct and operational.

### Manual Verification
- Start a new match and verify that the calculated `current_calculations.independent_analysis` blocks inside `data/chess_journal.json` successfully render the new blunder audit format in your glassmorphism web dashboard.
