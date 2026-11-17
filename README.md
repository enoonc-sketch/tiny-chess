# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/enoonc-sketch/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/enoonc-sketch/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4,096-byte Python chess engine for make.fun's tiny-chess-01 bounty.
Iterative-deepening alpha-beta with quiescence search, MVV-LVA move
ordering, and a material + piece-square evaluation — original code
written for this competition, standard library only.

## Engine

- 0x88 board, incremental evaluation (material + piece-square tables).
- Iterative deepening alpha-beta to a fixed node budget, so the run is
  deterministic: same position, same move — no clock, no randomness
  in the search.
- Quiescence search: captures, and all evasions when in check.
- Move ordering by MVV-LVA captures and promotions.
- Full rules: castling, en passant, promotion, checkmate/stalemate.
  The env adjudicates repetition, the fifty-move rule and time.

## The size rule

- `main.py` is the whole engine: 4,094 bytes as committed, Python 3.13,
  standard library only. It reads, imports or execs no other file.
- The rest of the tree (this README, LICENSE) keeps the whole snapshot
  under 8,192 bytes, no file over 4,096.

## Grade it locally

From the competition dev kit:

    makefun grade-local --kit . --bot <your repository> --driver docker

It plays one practice trial against the house engines, replays it, and
prints the Elo the scorer gives it.

<sub>Entered on [make.fun](https://make.fun/?ref=3n9mbbtb&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
