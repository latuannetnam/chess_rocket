# Chess Rocket - Setup Summary

**Date:** 2026-04-27

## Clone
```
https://github.com/suvojit-0x55aa/chess_rocket
```

## Dependencies
- `uv sync` — all 45 packages resolved (python-chess, mcp, rich, textual, etc.)
- Stockfish 16 at `/usr/games/stockfish`

## Data Initialized
- `data/sessions/`, `data/games/`, `data/lesson_plans/`
- `data/progress.json` and `data/srs_cards.json`
- Openings DB: 3,690 openings (SQLite + JSON trie)

## MCP Server
Configured in `.mcp.json` with correct `cwd` and `STOCKFISH_PATH` env var.

## Smoke Tests (all passed)
- `analyze_position` → 3 PV lines at depth 8 (top: +0.44)
- `evaluate_move` → e4 classified as "great", cp_loss=5
- `get_engine_move` at Elo 400/800/1320/1800 → different moves at each level

## Usage
- MCP server available when Claude Code loads this project
- Start game: `new_game(target_elo=800, player_color="white")`
- Dashboard: `uv run python scripts/dashboard_server.py`