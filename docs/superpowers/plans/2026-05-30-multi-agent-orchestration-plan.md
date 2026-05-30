# Multi-Agent Orchestration & Journal Partitioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a simulated Main Agent & Sub-Agent chess-playing protocol in live chat and partition the database `data/chess_journal.json` to cap active lessons at 5 compact rules while archiving older ones.

**Architecture:** We will manually restructure `chess_journal.json`, update the `tests/test_journal.py` test suite to assert the new schema, modify `scripts/dashboard.html` to render both active and archived lessons beautifully, and update `AGENTS.md` with the new multi-agent reasoning steps.

**Tech Stack:** Python, pytest, HTML/Javascript (Vanilla JS).

---

### Task 1: Restructure `data/chess_journal.json`

**Files:**
- Modify: `data/chess_journal.json`

- [ ] **Step 1: Overwrite `data/chess_journal.json` with the new partitioned schema containing the compacted active lessons and the complete archived lessons**

Replace the entire contents of `data/chess_journal.json` with the following migrated structure:

```json
{
  "total_games_played": 6,
  "current_learning_elo": 2000,
  "active_lessons": [
    {
      "id": "lesson_007",
      "motif": "Defended Pawn Capture Safety",
      "preventative_rule": "Never capture a defended pawn or piece with your last major piece when the defender (especially the enemy king) can capture it back, unless it leads to a forced winning endgame."
    },
    {
      "id": "lesson_008",
      "motif": "Insufficient Defender Calculation",
      "preventative_rule": "Before moving any piece to an active square, count all enemy attackers and your own defenders. If the opponent has more attackers than you have defenders, the square is unsafe."
    },
    {
      "id": "lesson_009",
      "motif": "Fork Vulnerability in Piece Relocation",
      "preventative_rule": "Avoid placing major or minor pieces on undefended squares where a single enemy piece (especially a long-range bishop or knight) can fork or double-attack them."
    },
    {
      "id": "lesson_010",
      "motif": "Queen Deflection and Intermediate Check",
      "preventative_rule": "Before initiating a forcing trade or capture sequence, verify if any of your other pieces depend on the capturing piece's defense. Check for intermediate checks (Zwischenzug) that can disrupt the sequence."
    },
    {
      "id": "lesson_011",
      "motif": "Pawn Attack Blindspot",
      "preventative_rule": "Always double-check the diagonal attack paths of all enemy pawns on adjacent files. Never move minor or major pieces to these squares unless they are sufficiently protected."
    }
  ],
  "archived_lessons": [
    {
      "id": "lesson_001",
      "timestamp": "2026-05-30T11:15:00Z",
      "game_id": "7e57d1ce-8e64-4c57-9074-b89e2c41261e",
      "elo_encountered": 1000,
      "motif": "Discovered Attacks & Checks",
      "concept": "Unleashing Hidden Long-Range Attackers",
      "mistake_description": "Recognized and utilized the Bg2 and f4 bishop diagonals to unleash crushing discovered attacks (Nd6+ on move 7 and e6+ on move 22).",
      "preventative_rule": "Always look for blocked diagonals or files containing enemy pieces (especially the Queen and King), and assess if moving the blocking piece creates high-tempo double attacks."
    },
    {
      "id": "lesson_002",
      "timestamp": "2026-05-30T11:15:30Z",
      "game_id": "7e57d1ce-8e64-4c57-9074-b89e2c41261e",
      "elo_encountered": 1000,
      "motif": "Overloaded Defenses",
      "concept": "Targeting Multi-Attacked Squares",
      "mistake_description": "Identified that e5 was overloaded after Ne5 blocked the check, leading to a forcing capturing sequence.",
      "preventative_rule": "Count the number of active attackers and defenders on a key central square before initiating a capture sequence to ensure a net material advantage."
    },
    {
      "id": "lesson_003",
      "timestamp": "2026-05-30T11:34:00Z",
      "game_id": "13398c1c-c7af-4348-81c3-25660f701b3e",
      "elo_encountered": 2000,
      "motif": "Mating Nets in Knight Endgames",
      "concept": "Avoid Self-Trapping Blockades",
      "mistake_description": "Allowed the king to get blockaded on d1 and c1, leading to a forced checkmate net with d2+ and Nc3#.",
      "preventative_rule": "Never blockade an enemy passed pawn on the back rank if the enemy king and knight can trap your king. Active king play and counter-threats are mandatory to avoid self-trapping."
    },
    {
      "id": "lesson_004",
      "timestamp": "2026-05-30T11:53:00Z",
      "game_id": "d5273222-a698-476a-a508-2f7dd17dd955",
      "elo_encountered": 2000,
      "motif": "Defensive Pawn Capture Safety",
      "concept": "Verifying Square Defenders before Capturing",
      "mistake_description": "Captured a defended passed pawn on d4 with 34. Qxd4??, overlooking that the Knight on e7 and the Queen defended it, leading to the immediate loss of the Queen.",
      "preventative_rule": "Never capture an enemy passed pawn or piece in the center without double-checking all direct and indirect defenders, ensuring the capturing piece is sufficiently protected."
    },
    {
      "id": "lesson_005",
      "timestamp": "2026-05-30T11:53:00Z",
      "game_id": "d5273222-a698-476a-a508-2f7dd17dd955",
      "elo_encountered": 2000,
      "motif": "Desperado Rook Blunder",
      "concept": "Maintaining Composition Under Material Disadvantage",
      "mistake_description": "After losing the Queen, played 35. Rd1??, hanging the Rook to Qxd1+ in a desperado attempt to attack, instead of trying to defend or consolidate the remaining material.",
      "preventative_rule": "When experiencing a severe material loss, do not panic or play high-risk desperado moves that hang remaining major pieces. Focus on defensive resilience, slow down, and verify square safety."
    },
    {
      "id": "lesson_006",
      "timestamp": "2026-05-30T12:45:00Z",
      "game_id": "bfae7bc6-71ab-4209-809d-4160ad6d4f89",
      "elo_encountered": 2000,
      "motif": "Undefended Adjacent Checks",
      "concept": "Verifying Guard Protection for Close-Range Attacks",
      "mistake_description": "Played 65. Qb2+?? checking the king on c1 but placing the Queen on b2 with zero defender protection, allowing the enemy king to capture it (Kxb2) and promote to win the game.",
      "preventative_rule": "When checking the enemy king from an adjacent square, always ensure the attacking piece is defended by your king or another piece. An undefended piece adjacent to the king will be captured immediately."
    },
    {
      "id": "lesson_007",
      "timestamp": "2026-05-30T12:45:15Z",
      "game_id": "bfae7bc6-71ab-4209-809d-4160ad6d4f89",
      "elo_encountered": 2000,
      "motif": "Defended Pawn Capture Safety",
      "concept": "Checking Defending Range of King",
      "mistake_description": "Captured a pawn on f6 with 45. Rxf6?? when the enemy king on e7 was adjacent to f6, hanging our last rook to Kxf6.",
      "preventative_rule": "Never capture a defended pawn or piece with your last major piece when the defender (especially the enemy king) can capture it back, unless it leads to a forced winning endgame."
    },
    {
      "id": "lesson_008",
      "timestamp": "2026-05-30T13:00:00Z",
      "game_id": "74dff5a8-6d6c-4e30-b6c6-f7c5373f725f",
      "elo_encountered": 2000,
      "motif": "Insufficient Defender Calculation",
      "concept": "Square Safety and Attacker/Defender Ratio",
      "mistake_description": "Played 16. Bf4??, moving a light-squared bishop to a square attacked twice (Queen on d6 and Bishop on e6) and defended only once (Queen on d2), leading to immediate material loss.",
      "preventative_rule": "Before moving any piece to an active square, count all enemy attackers and your own defenders. If the opponent has more attackers than you have defenders, the square is unsafe."
    },
    {
      "id": "lesson_009",
      "timestamp": "2026-05-30T13:00:15Z",
      "game_id": "74dff5a8-6d6c-4e30-b6c6-f7c5373f725f",
      "elo_encountered": 2000,
      "motif": "Fork Vulnerability in Piece Relocation",
      "concept": "Keeping Minor/Major Pieces Defended",
      "mistake_description": "Allowed 24... Bd2 double-attacking two undefended knights (c3 and e1) after trading rooks on e1, leading to the loss of a second minor piece.",
      "preventative_rule": "Avoid placing major or minor pieces on undefended squares where a single enemy piece (especially a long-range bishop or knight) can fork or double-attack them."
    },
    {
      "id": "lesson_010",
      "timestamp": "2026-05-30T14:15:00Z",
      "game_id": "d9fc3cc1-f6d0-4cad-91c4-702ea05f40f0",
      "elo_encountered": 2000,
      "motif": "Queen Deflection and Intermediate Check",
      "concept": "Verifying Defended Pieces During Forcing Trades",
      "mistake_description": "Captured Black's queen with 39. Qxb6??, deflecting our own queen from defending our rook on d1. This allowed Black to play the intermediate check 39... Rxd1+!, winning the rook and then recapturing on b6.",
      "preventative_rule": "Before initiating a forcing trade or capture sequence, verify if any of your other pieces depend on the capturing piece's defense. Check for intermediate checks (Zwischenzug) that can disrupt the sequence."
    },
    {
      "id": "lesson_011",
      "timestamp": "2026-05-30T14:15:30Z",
      "game_id": "d9fc3cc1-f6d0-4cad-91c4-702ea05f40f0",
      "elo_encountered": 2000,
      "motif": "Pawn Attack Blindspot",
      "concept": "Double-Checking Pawn Diagonals",
      "mistake_description": "Placed our bishop on e4 with 42. Be4??, failing to calculate that Black's d5 pawn attacked the e4 square diagonally forward, leading to the immediate capture of our bishop (42... dxe4).",
      "preventative_rule": "Always double-check the diagonal attack paths of all enemy pawns on adjacent files. Never move minor or major pieces to these squares unless they are sufficiently protected."
    }
  ],
  "current_calculations": {
    "current_game_id": "23efad6b-91b7-403b-a789-1f19b0821e80",
    "last_move_played": "Nd3",
    "independent_analysis": "### 🧠 Pre-Move Analysis (Move 20)\n*   **Active Lessons Applied**: [lesson_007, lesson_008, lesson_009, lesson_010, lesson_011]\n*   **Opponent's Threats**: Black played 19... Be7, preparing to castle.\n*   **Candidate Moves & Blunder-Prevention Audit**:\n    1. Nd3\n       - *Blunder Audit*: Passed.\n       - *Pros/Cons*: Pro: Positionally flawless, eyes c5. Con: None.\n*   **Calculation Line**:\n    *   *If I play Nd3 -> Black castles (O-O)*\n*   **Safety Checklist**:\n    *   [x] Stored lessons blunder audit passed.\n    *   [x] Target square safe.\n*   **Decision**: Play Nd3",
    "pre_move_checklist_passed": true
  }
}
```

- [ ] **Step 2: Commit changes to git**

Run:
```bash
git add data/chess_journal.json
git commit -m "refactor: restructure chess_journal.json into active and archived partitions"
```

---

### Task 2: Update the Test Suite (`tests/test_journal.py`)

**Files:**
- Modify: `tests/test_journal.py`

- [ ] **Step 1: Write the failing tests**

Modify `tests/test_journal.py` to replace `lessons_learned` expectations with the new `active_lessons` and `archived_lessons` fields. Replace lines 34 to 84 with:

```python
def test_journal_schema_structure(temp_journal_cleaner):
    """Verify that chess_journal.json is in valid JSON format and has the required schema."""
    # Write a test journal
    test_data = {
        "total_games_played": 1,
        "current_learning_elo": 1000,
        "active_lessons": [
            {
                "id": "lesson_001",
                "motif": "Open File Danger",
                "preventative_rule": "Look before you leap."
            }
        ],
        "archived_lessons": [
            {
                "id": "lesson_001",
                "timestamp": "2026-05-30T10:15:30Z",
                "game_id": "test_game_123",
                "elo_encountered": 1000,
                "motif": "Open File Danger",
                "concept": "Hanging Queens to Active Rooks",
                "mistake_description": "Captured a pawn blindly.",
                "preventative_rule": "Look before you leap."
            }
        ],
        "current_calculations": {
            "current_game_id": "test_game_123",
            "last_move_played": "e4",
            "independent_analysis": "White plays e4, fighting for center.",
            "pre_move_checklist_passed": True
        }
    }
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _JOURNAL_PATH.write_text(json.dumps(test_data, indent=2), encoding="utf-8")

    # Read and parse
    read_data = json.loads(_JOURNAL_PATH.read_text(encoding="utf-8"))
    assert read_data["total_games_played"] == 1
    assert len(read_data["active_lessons"]) == 1
    assert len(read_data["archived_lessons"]) == 1
    assert read_data["current_calculations"]["pre_move_checklist_passed"] is True
    assert read_data["current_calculations"]["last_move_played"] == "e4"
```

Also, update `test_dashboard_handler_api_journal` to use the new schema:

```python
def test_dashboard_handler_api_journal(temp_journal_cleaner):
    """Test that the DashboardHandler serves the journal correctly via /api/journal."""
    test_data = {
        "total_games_played": 2,
        "current_learning_elo": 1200,
        "active_lessons": [],
        "archived_lessons": [],
        "current_calculations": {
            "current_game_id": None,
            "last_move_played": None,
            "independent_analysis": "Initial state",
            "pre_move_checklist_passed": False
        }
    }
```

- [ ] **Step 2: Run unit tests to verify they pass**

Run:
```bash
uv run pytest tests/test_journal.py
```
Expected output:
```
tests/test_journal.py ..                                                 [100%]
======= 2 passed in 0.05s =======
```

- [ ] **Step 3: Commit changes to git**

Run:
```bash
git add tests/test_journal.py
git commit -m "test: update test_journal.py to validate partitioned active/archived schema"
```

---

### Task 3: Update `scripts/dashboard.html` to Render Partitioned Lessons

**Files:**
- Modify: `scripts/dashboard.html:619-640`

- [ ] **Step 1: Modify `scripts/dashboard.html` to render both `active_lessons` (compacted format) and `archived_lessons` (detailed format) with custom visually distinct headings and border styles**

Replace lines 619 to 640 of `scripts/dashboard.html` with:

```javascript
      // Update lessons
      const lessonsEl = document.getElementById('journal-lessons');
      if (lessonsEl) {
        let html = '';
        if (journal.active_lessons && journal.active_lessons.length > 0) {
          html += '<h3 style="font-size: 0.95rem; color: var(--yellow); margin-top: 0; margin-bottom: 10px;">🎯 Active Lessons (Audited in Play)</h3>';
          journal.active_lessons.forEach(lesson => {
            html += '<div class="lesson-card" style="border-left: 3px solid var(--yellow); margin-bottom: 12px; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 4px;">';
            html += '  <div class="lesson-header" style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-dim); margin-bottom: 6px;">';
            html += '    <span class="lesson-motif" style="background: rgba(234,179,8,0.1); color: var(--yellow); padding: 2px 6px; border-radius: 3px; font-weight: 600;">' + esc(lesson.motif || 'Tactics') + '</span>';
            html += '    <span>Active</span>';
            html += '  </div>';
            html += '  <div class="lesson-rule" style="font-size: 0.85rem; font-style: italic; color: var(--text-light);">💡 ' + esc(lesson.preventative_rule || '') + '</div>';
            html += '</div>';
          });
        }
        
        if (journal.archived_lessons && journal.archived_lessons.length > 0) {
          html += '<h3 style="font-size: 0.95rem; color: var(--text-dim); margin-top: 20px; margin-bottom: 10px;">📦 Archived Lessons</h3>';
          journal.archived_lessons.forEach(lesson => {
            html += '<div class="lesson-card" style="opacity: 0.7; border-left: 3px solid var(--text-dim); margin-bottom: 12px; padding: 12px; background: rgba(255,255,255,0.02); border-radius: 4px;">';
            html += '  <div class="lesson-header" style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-dim); margin-bottom: 6px;">';
            html += '    <span class="lesson-motif" style="background: rgba(255,255,255,0.05); color: var(--text-dim); padding: 2px 6px; border-radius: 3px;">' + esc(lesson.motif || 'Tactics') + '</span>';
            html += '    <span>Elo: ' + esc(lesson.elo_encountered || 1000) + '</span>';
            html += '  </div>';
            html += '  <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-dim); margin-bottom: 4px;">' + esc(lesson.concept || 'Mistake') + '</div>';
            html += '  <div class="lesson-desc" style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 6px; line-height: 1.3;">' + esc(lesson.mistake_description || '') + '</div>';
            html += '  <div class="lesson-rule" style="font-size: 0.8rem; font-style: italic; color: var(--text-dim);">💡 ' + esc(lesson.preventative_rule || '') + '</div>';
            html += '</div>';
          });
        }
        
        if (!html) {
          lessonsEl.innerHTML = '<div style="font-size: 0.8rem; color: var(--text-dim); text-align: center; padding: 20px 0;">No active lessons learned yet. Play games to train!</div>';
        } else {
          lessonsEl.innerHTML = html;
        }
      }
```

- [ ] **Step 2: Commit changes to git**

Run:
```bash
git add scripts/dashboard.html
git commit -m "feat: render active and archived lessons partitions in the dashboard server TUI/HTML"
```

---

### Task 4: Update the System Rules in `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Update the game lifecycle, pre-move protocol, and post-game rules in `AGENTS.md` to establish the simulated Main Agent / Sub-Agent structure and partitioned journal handling**

Replace lines 34 to 84 of `AGENTS.md` with:

```markdown
## Game Lifecycle & Persistence Protocol

To support continuous self-improvement across sessions, the **Main Agent** manages the persistent journal database located at `data/chess_journal.json`.

### 1. Pre-Game: Load Memory & Lessons
Before calling `new_game` to start a match:
1. Read the contents of `data/chess_journal.json`.
2. Print a neat summary of all `active_lessons` (the active cap of 5 rules) in the chat.
3. Keep these preventative rules in active context to avoid repeating past blunders.

### 2. Pre-Move Calculation Protocol
Before playing any move using the `make_move` tool:
1. Run a simulated multi-agent sequential analysis involving specialized Sub-Agents managed by the Main Agent.
2. Output a structured multi-agent coordination block in the chat in the format below.
3. Write the exact analysis block to `current_calculations.independent_analysis` in `data/chess_journal.json`, and set `current_calculations.pre_move_checklist_passed` to `true` (once all checks are done), `current_calculations.current_game_id` to the active `game_id`, and `current_calculations.last_move_played` to your selected move.

**Pre-Move Calculation Block Format:**
```markdown
### 👑 Main Agent: Move X Planning
*   **Active Lessons Loaded**: [List all active lesson IDs from active_lessons]

#### ♟️ [Sub-Agent: Positional Strategist]
*   **Positional Assessment**: [Evaluate long-term structures, space advantages, king safety, and plans]
*   **Key Squares/Targets**: [List vital squares or pieces to target or defend]

#### ⚔️ [Sub-Agent: Tactical Calculator]
*   **Opponent's Threats**: [Analyze what Stockfish's last move threatens]
*   **Candidate Moves**:
    1. [Move A] - *Line*: [A -> B -> C] - *Pros/Cons*: [Quick assessment]
    2. [Move B] - *Line*: [X -> Y -> Z] - *Pros/Cons*: [Quick assessment]

#### 🔍 [Sub-Agent: Blunder Auditor]
*   **Audit against Active Lessons**:
    - [Move A] -> [Blunder Audit vs active_lessons (e.g., Safe from forks? Yes. Defended? Yes.)]
    - [Move B] -> [Blunder Audit vs active_lessons]
*   **Safety Checklist**:
    - [x] Stored lessons blunder audit passed for the selected move.
    - [x] Target square is safe and not attacked by hidden long-range pieces.
    - [x] No hanging major pieces.
    - [x] King safety / back-rank checkmate threats assessed.

#### 👑 [Main Agent: Final Synthesis]
*   **Decision**: Play [Selected Move]
```

### 3. Post-Game Self-Analysis Protocol
When `is_game_over: true`, the game has ended:
1. Review the full game move history.
2. Identify 1-3 key tactical turning points or calculation mistakes where thinking failed.
3. Formulate generalized **Preventative Rules** to avoid similar blunders in the future.
4. Update `data/chess_journal.json`:
   - Increment `total_games_played` by `1`.
   - Update `current_learning_elo` to the rating of the opponent played.
   - For each new lesson, add it in compact format to `active_lessons` (`id`, `motif`, `preventative_rule`). Also append it in full metadata format to `archived_lessons` (`id`, `timestamp`, `game_id`, `elo_encountered`, `motif`, `concept`, `mistake_description`, `preventative_rule`).
   - If the size of `active_lessons` exceeds **5**, pop the oldest lessons from `active_lessons` until the size is exactly 5.
   - Reset `current_calculations` properties (`current_game_id`, `last_move_played` to `null`, `independent_analysis` to `"Initial state: Waiting for first move."`, and `pre_move_checklist_passed` to `false`).
5. Share your post-game self-analysis and the newly saved lessons in the chat.
```

- [ ] **Step 2: Commit changes to git**

Run:
```bash
git add AGENTS.md
git commit -m "docs: update AGENTS.md instructions to enforce Main/Sub-agent sequence and partitioned database lifecycle"
```
