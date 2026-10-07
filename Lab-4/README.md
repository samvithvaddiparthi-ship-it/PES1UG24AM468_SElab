# Lab 4 - Vibe Coding

**Name:** Samvith Vaddiparthi  
**SRN:** PES1UG24AM468  
**Section:** H  
**Assigned repo:** Scenario 19 - Battleship vs AI (https://github.com/SETAPESU26/19_battleship)  
**LLM used:** Claude (Claude Code, Claude Opus 5.5)

## Contents
| Item | File |
| --- | --- |
| Video before changes (bugs visible) | `videos/PES1UG24AM468_before.mp4` |
| Video after changes (fixes + Tasks 1-4) | `videos/PES1UG24AM468_after.mp4` |
| Updated code | `code/` |
| Chat history (exported) | `PES1UG24AM468_Lab4_chat_history.pdf` |

## Bugs shown in the before video
- The same cell (`3,3`) can be fired at twice and is counted as a HIT both times.
- "Ship cells remaining" stays at 3 even after hits (it checked the wrong board).
- The AI fires at `1,1` (empty) and the game says "AI scored a hit" - the AI's 1-based
  text was compared with 0-based ship cells. AI shots were never applied to the player's board.

## What the after video shows
- Side-by-side boards (`X` hit, `o` miss, `#` sunk, `S` your ship) and ships afloat.
- One feedback line per real shot, e.g. `You fire at 3,5: HIT! You sank the enemy Cruiser!`
- Repeated (`3,3`) and off-board (`9,9`) shots rejected without using a turn.
- AI hunt/target: after hitting `5,5` it tries the neighbouring cells and sinks the Destroyer.
- Three ships per side; the game ends with a win when the enemy fleet is sunk.

## Tasks (one commit each in the code repo)
1. Consistent coordinate handling (`coords.py`, 0-based tuples internally).
2. Fleet of ships, per-ship damage, sunk ships, repeated-shot prevention, win/lose.
3. Hunt/target AI that never repeats a cell and handles no remaining choices.
4. Hit/miss/sunk feedback exactly once per actual shot; AI selection is silent.

## Run
```bash
cd code
python3 main.py
python3 -m unittest -v   # 39 tests, standard library only
```
