# Scenario 19 — Battleship vs AI

A terminal Battleship game with separate board and AI modules.

## Provided files

- `main.py` — entry point.
- `game.py` — turn flow and setup.
- `board.py` — ship and shot state.
- `ai.py` — computer targeting.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

## Before changing the code

Inspect how coordinates are represented in every module. Fire at known ship cells and
known empty cells. Then trace an AI shot from selection to hit detection.

## Task 1 — Consistent coordinate handling

Make coordinate representation consistent across input, ship placement, player shots,
and AI shots so occupied cells are recognised correctly.

**Done when:** every real ship coordinate is treated as a hit and every known empty
coordinate is treated as a miss.

## Task 2 — Complete fleet and win logic

Support multiple ships, track individual ship damage, identify sunk ships, prevent
repeated shots, and end the game when the fleet is sunk.

## Task 3 — Improve the AI

After a hit, make the AI preferentially consider nearby untried cells. It must never
shoot the same coordinate twice and must handle a board with no remaining choices.

## Task 4 — Shot-level feedback

Ensure hit/miss/sunk feedback occurs exactly once for an actual shot. Internal AI
candidate selection must not produce false hit/miss messages.

## Required testing

Test hits, misses, repeated shots, sinking one ship, sinking all ships, AI repeated-shot
prevention, adjacent targeting after a hit, invalid coordinates, and quitting.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [ ] Task 1 completed and the original defect was reproduced and fixed.
- [ ] Tasks 2–4 completed and tested.
- [ ] Boundary and invalid-input cases tested.
- [ ] No unnecessary external dependencies added.
- [ ] No persistent storage added.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-07-battleship/
├── README.md
├── requirements.txt
├── main.py
├── game.py
├── board.py
└── ai.py
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

---

## Solution notes — Samvith Vaddiparthi (PES1UG24AM468)

### Original defects found
- `ai.py` returned 1-based text (`"1,1"`) that `game.py` compared to 0-based ship
  cells, so the AI "hit" empty cells and missed real ones. AI shots were also never
  recorded on the player's board, so the AI could never win.
- The repeated-shot check and "Ship cells remaining" looked at the player's board
  instead of the enemy board: the same cell could be fired at (and "HIT") again and
  the remaining count never went down.

### What changed (one commit per task)
| Task | Change |
| --- | --- |
| 1 | `coords.py` is the single source of truth: 0-based `(row, col)` tuples everywhere, converted to/from 1-based `row,col` text only at input/output. |
| 2 | `Ship` objects with per-ship hits, 3 ships per side, placement validation, `ShotResult` with sunk ship, `RepeatedShotError`, win **and** lose conditions, `q`/`quit`/`exit`/Ctrl+D to quit. |
| 3 | Hunt/target AI: after a hit it tries untried neighbours, follows a line after two hits, forgets hits on sunk ships, never repeats a cell, returns `None` when no cells remain. |
| 4 | Exactly one feedback line per real shot (`You fire at 3,5: HIT! You sank the enemy Cruiser!`), silent AI selection, AI misses reported, side-by-side board display. |

Board key: `X` hit, `o` miss, `#` sunk ship, `S` your undamaged ship, `.` water.

### Running the tests
Standard library only (no extra dependencies, no persistent storage):

```bash
python3 -m unittest -v
```

The tests cover hits, misses, repeated shots, sinking one ship, sinking all ships
(both sides), AI repeated-shot prevention, adjacent targeting after a hit, a board
with no choices left, invalid coordinates, quitting, and one-message-per-shot feedback.

### Updated folder structure
```text
19_battleship/
├── README.md
├── requirements.txt
├── main.py
├── game.py      # turn flow, input, feedback, display
├── board.py     # Ship, ShotResult, Board
├── ai.py        # hunt/target AI
├── coords.py    # coordinate parsing/formatting
└── tests/       # unittest suite for Tasks 1-4
```
