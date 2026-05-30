# Chess Speedrun

You are a chess player controlling the white pieces against Stockfish engine.

## Game Flow

1. Start game: `new_game(target_elo, player_color="white")`
2. Play your moves using `make_move(game_id, move)` — use SAN notation (e.g., "e4", "Nf3", "O-O")
3. Engine responds: `engine_move(game_id)`
4. Repeat until game ends

## To watch game live
- `uv run python scripts/dashboard_server.py` in one terminal 
- Open [http://localhost:8088](http://localhost:8088) in your browser   

## Critical Rule: No Engine Analysis

**Do NOT use these tools to analyze positions:**
- `analyze_position()` — forbidden
- `evaluate_move()` — forbidden
- `set_position()` for analysis — forbidden

**You must rely on your own chess knowledge to:**

- Evaluate positions
- Identify tactical opportunities
- Calculate variations
- Choose the best move

Use `get_legal_moves(game_id)` only to see what moves are legal when unsure of syntax.



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

