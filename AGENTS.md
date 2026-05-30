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
1. Run the print subcommand of our journal tool: `uv run python scripts/update_journal.py print-lessons`
2. Print the exact printed output directly in the chat to maintain context.
3. Keep these preventative rules in active context to avoid repeating past blunders.

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

Output the structured results in the chat. Write the exact synthesized block to the journal by running the update command with a shell Heredoc (replacing `<game_id>`, `<move>`, and the block body content accordingly):

```bash
uv run python scripts/update_journal.py pre-move --game-id "<game_id>" --move "<move>" << 'EOF'
[Insert exact synthesized block here]
EOF
```

**Pre-Move Calculation Block Format:**
```markdown
### 👑 Main Agent: Move X Planning
*   **Active Lessons Loaded**: [List all active lesson IDs from active_lessons]

#### ♟️ [Sub-Agent: Positional Strategist] - Tool Call: `invoke_subagent(Role="Positional Strategist", ...)`
*   **Positional Assessment**: [Direct output from the Positional Strategist sub-agent]

#### ⚔️ [Sub-Agent: Tactical Calculator] - Tool Call: `invoke_subagent(Role="Tactical Calculator", ...)`
*   **Opponent's Threats**: [Direct threat assessment from the Tactical Calculator sub-agent]
*   **Candidate Moves**:
    1. [Move A] - *Line*: [A -> B -> C] - *Pros/Cons*: [Calculation from sub-agent]
    2. [Move B] - *Line*: [X -> Y -> Z] - *Pros/Cons*: [Calculation from sub-agent]

#### 🔍 [Sub-Agent: Blunder Auditor] - Tool Call: `invoke_subagent(Role="Blunder Auditor", ...)`
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
4. Update `data/chess_journal.json` safely by running our database utility:
   - Write the mistake description to a temporary file `temp_mistake.txt`.
   - Update the database by running:
     `uv run python scripts/update_journal.py post-game --game-id "<game_id>" --elo <elo> --motif "<motif>" --concept "<concept>" --rule "<preventative_rule>" < temp_mistake.txt`
   - Delete `temp_mistake.txt` once the transaction finishes successfully.
5. Share your post-game self-analysis and the newly saved lessons in the chat.

