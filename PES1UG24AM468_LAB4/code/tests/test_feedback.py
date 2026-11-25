"""Task 4: hit/miss/sunk feedback appears exactly once per actual shot."""
import contextlib
import io
import random
import re
import unittest

from ai import AI
from board import Board
from coords import format_coord
from game import ENEMY_FLEET, PLAYER_FLEET, Battleship
from tests.helpers import ScriptedAI, play, scripted_input

SHOT_LINE = re.compile(r"^(?:> )?(You fire|AI fires) at (\d,\d): (miss\.|HIT!.*)$")
ENEMY_CELLS = [cell for cells in ENEMY_FLEET.values() for cell in cells]


def shot_lines(out):
    return [m.groups() for m in map(SHOT_LINE.match, out.splitlines()) if m]


class FeedbackTests(unittest.TestCase):
    def test_one_line_per_real_shot_in_a_full_game(self):
        for seed in range(10):
            with self.subTest(seed=seed):
                misses = [format_coord((r, c)) for r in range(6) for c in range(6)
                          if (r, c) not in ENEMY_CELLS]
                rng = random.Random(seed)
                rng.shuffle(misses)
                moves = misses[:8] + [format_coord(c) for c in ENEMY_CELLS]
                game = Battleship(ai=AI(rng=random.Random(seed)), input_func=scripted_input(moves))
                outcome, out = play(game)
                lines = shot_lines(out)
                player = [pos for who, pos, _ in lines if who == "You fire"]
                ai = [pos for who, pos, _ in lines if who == "AI fires"]
                # Exactly one announcement for every cell fired at, no more.
                self.assertEqual(sorted(player), sorted(map(format_coord, game.enemy.shots)))
                self.assertEqual(sorted(ai), sorted(map(format_coord, game.player.shots)))
                self.assertEqual(len(player), len(set(player)))
                self.assertEqual(len(ai), len(set(ai)))
                self.assertEqual(out.count("HIT!") + out.count("miss."), len(lines))

    def test_announced_result_matches_the_board(self):
        game = Battleship(ai=AI(rng=random.Random(4)),
                          input_func=scripted_input([format_coord(c) for c in ENEMY_CELLS]))
        _, out = play(game)
        for who, pos, verdict in shot_lines(out):
            board = game.enemy if who == "You fire" else game.player
            cell = (int(pos[0]) - 1, int(pos[2]) - 1)
            self.assertEqual(verdict.startswith("HIT!"), cell in board.ships, (who, pos))

    def test_sunk_announced_once_on_the_sinking_shot(self):
        moves = ["5,1", "6,1"]  # enemy Destroyer at (4, 0) and (5, 0)
        game = Battleship(ai=ScriptedAI([(0, 0), (0, 1)]), input_func=scripted_input(moves))
        _, out = play(game)
        self.assertEqual(out.count("sank the enemy Destroyer"), 1)
        self.assertIn("You fire at 6,1: HIT! You sank the enemy Destroyer!", out)
        self.assertIn("You fire at 5,1: HIT!\n", out)

    def test_ai_sinking_message(self):
        ai = ScriptedAI([(5, 0), (5, 1)])  # player Patrol Boat
        game = Battleship(ai=ai, input_func=scripted_input(["1,1", "1,2"]))
        _, out = play(game)
        self.assertIn("AI fires at 6,1: HIT!\n", out)
        self.assertIn("AI fires at 6,2: HIT! AI sank your Patrol Boat!", out)
        self.assertEqual(out.count("sank your Patrol Boat"), 1)

    def test_ai_candidate_selection_prints_nothing(self):
        board = Board()
        for name, cells in PLAYER_FLEET.items():
            board.place_ship(name, cells)
        ai = AI(rng=random.Random(2))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            for _ in range(Board.SIZE * Board.SIZE):
                pos = ai.choose()
                ai.record(pos, board.fire(pos))
            ai.choose()  # no cells left
        self.assertEqual(out.getvalue(), "")

    def test_rejected_input_gives_no_hit_or_miss(self):
        moves = ["3,3", "3,3", "0,4", "x", "q"]
        game = Battleship(ai=ScriptedAI([(0, 0)]), input_func=scripted_input(moves))
        _, out = play(game)
        self.assertEqual(shot_lines(out), [("You fire", "3,3", "HIT!"),
                                           ("AI fires", "1,1", "miss.")])

    def test_board_shows_hits_misses_and_sunk(self):
        board = Board()
        board.place_ship("Patrol Boat", [(0, 0), (0, 1)])
        board.place_ship("Destroyer", [(2, 2), (3, 2)])
        board.fire((2, 2))  # hit
        board.fire((5, 5))  # miss
        board.fire((0, 0))
        board.fire((0, 1))  # sinks Patrol Boat
        hidden = board.render(reveal_ships=False)
        self.assertEqual(hidden[1], " 1 # # . . . .")
        self.assertEqual(hidden[3], " 3 . . X . . .")
        self.assertEqual(hidden[4], " 4 . . . . . .")  # unhit ship stays hidden
        self.assertEqual(hidden[6], " 6 . . . . . o")
        self.assertEqual(board.render(reveal_ships=True)[4], " 4 . . S . . .")


if __name__ == "__main__":
    unittest.main()
