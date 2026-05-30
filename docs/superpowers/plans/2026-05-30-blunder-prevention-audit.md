# Active Blunder-Prevention Audit System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce a strict blunder-prevention audit on all candidate moves in the agent's pre-move chess lifecycle.

**Architecture:** We will modify `AGENTS.md` to update the Pre-Move Calculation Protocol, changing the unstructured candidate list into a structured Candidate Move Blunder-Prevention Audit checklist.

**Tech Stack:** Markdown

---

### Task 1: Update Agent Instructions

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Modify the Pre-Move Calculation Block in AGENTS.md**
  
  Edit the Pre-Move Calculation Block Format to require auditing each candidate move against all active lessons in the journal database.

- [ ] **Step 2: Commit the changes**

  Run:
  ```bash
  git add AGENTS.md
  git commit -m "docs: update agent instructions with active blunder-prevention audit protocol"
  ```
  Expected: Successful commit.
