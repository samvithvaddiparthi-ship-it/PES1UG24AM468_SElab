"""Task 2: multiple ships, per-ship damage, sinking, repeat shots, win/lose."""
import unittest

from board import Board, RepeatedShotError
from coords import format_coord
from game import ENEMY_FLEET, PLAYER_FLEET, Battleship
from tests.helpers import ScriptedAI, play, scripted_input

ENEMY_CELLS = [cell for cells in ENEMY_FLEET.values() for cell in cells]
PLAYER_CELLS = [cell for cells in PLAYER_FLEET.values() for cell in cells]
# Cells with no ship on either board, used as harmless "misses".
EMPTY = [(r, c) for r in range(Board.SIZE) for c in range(Board.SIZE)
         if (r, c) not in ENEMY_CELLS and (r, c) not in PLAYER_CELLS]


def text(cells):
    return [format_coord(cell) for cell in cells]


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.cruiser = self.board.place_ship("Cruiser", [(0, 0), (0, 1), (0, 2)])
        self.destroyer = self.board.place_ship("Destroyer", [(2, 0), (3, 0)])

    def test_hit_and_miss(self):
        self.assertTrue(self.board.fire((0, 1)).hit)
        self.assertFalse(self.board.fire((5, 5)).hit)

    def test_damage_is_tracked_per_ship(self):
        self.board.fire((0, 0))
        self.board.fire((2, 0))
        self.assertEqual(self.cruiser.hits, {(0, 0)})
        self.assertEqual(self.destroyer.hits, {(2, 0)})

    def test_sinking_one_ship(self):
        self.assertIsNone(self.board.fire((2, 0)).sunk_ship)
        result = self.board.fire((3, 0))
        self.assertIs(result.sunk_ship, self.destroyer)
        self.assertTrue(self.destroyer.sunk)
        self.assertFalse(self.cruiser.sunk)
        self.assertFalse(self.board.all_sunk())
        self.assertEqual(self.board.ships_afloat(), [self.cruiser])

    def test_sinking_all_ships(self):
        for cell in [(0, 0), (0, 1), (0, 2), (2, 0), (3, 0)]:
            self.board.fire(cell)
        self.assertTrue(self.board.all_sunk())

    def test_repeated_shot_rejected_and_not_counted(self):
        self.board.fire((0, 0))
        with self.assertRaises(RepeatedShotError):
            self.board.fire((0, 0))
        self.assertEqual(self.cruiser.hits, {(0, 0)})
        self.board.fire((5, 5))
        with self.assertRaises(RepeatedShotError):
            self.board.fire((5, 5))

    def test_shot_outside_board_rejected(self):
        with self.assertRaises(ValueError):
            self.board.fire((6, 0))

    def test_invalid_placements_rejected(self):
        for name, cells in [("Overlap", [(0, 2), (1, 2)]),
                            ("Outside", [(5, 5), (5, 6)]),
                            ("Diagonal", [(4, 4), (5, 5)]),
                            ("Gap", [(5, 0), (5, 2)]),
                            ("Empty", [])]:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    self.board.place_ship(name, cells)

    def test_empty_board_is_not_sunk(self):
        self.assertFalse(Board().all_sunk())


class GameFlowTests(unittest.TestCase):
    def test_game_sets_up_multiple_ships(self):
        game = Battleship()
        self.assertEqual(len(game.player.fleet), 3)
        self.assertEqual(len(game.enemy.fleet), 3)

    def test_player_wins_when_enemy_fleet_sunk(self):
        game = Battleship(ai=ScriptedAI(EMPTY), input_func=scripted_input(text(ENEMY_CELLS)))
        outcome, out = play(game)
        self.assertEqual(outcome, "player")
        for name in ENEMY_FLEET:
            self.assertIn(f"You sank the enemy {name}!", out)
        self.assertIn("You win!", out)

    def test_game_ends_immediately_after_last_ship(self):
        # Extra input after the winning shot must never be read.
        moves = text(ENEMY_CELLS) + ["1,1"]
        game = Battleship(ai=ScriptedAI(EMPTY), input_func=scripted_input(moves))
        outcome, _ = play(game)
        self.assertEqual(outcome, "player")
        self.assertNotIn((0, 0), game.enemy.shots)

    def test_ai_wins_when_player_fleet_sunk(self):
        misses = text(EMPTY[:len(PLAYER_CELLS)])
        game = Battleship(ai=ScriptedAI(PLAYER_CELLS), input_func=scripted_input(misses))
        outcome, out = play(game)
        self.assertEqual(outcome, "ai")
        for name in PLAYER_FLEET:
            self.assertIn(f"AI sank your {name}!", out)
        self.assertIn("You lose.", out)

    def test_repeated_player_shot_does_not_use_a_turn(self):
        game = Battleship(ai=ScriptedAI(EMPTY), input_func=scripted_input(["3,3", "3,3", "q"]))
        outcome, out = play(game)
        self.assertEqual(outcome, "quit")
        self.assertIn("Already fired at 3,3", out)
        self.assertEqual(out.count("HIT!"), 1)
        self.assertEqual(len(game.player.shots), 1)  # AI got exactly one turn

    def test_invalid_input_does_not_use_a_turn(self):
        moves = ["", "abc", "1,2,3", "0,0", "7,7", "q"]
        game = Battleship(ai=ScriptedAI(EMPTY), input_func=scripted_input(moves))
        outcome, out = play(game)
        self.assertEqual(outcome, "quit")
        self.assertEqual(game.enemy.shots, set())
        self.assertEqual(game.player.shots, set())
        self.assertIn("Outside board", out)

    def test_quit_words_and_end_of_input(self):
        for moves in (["q"], ["Q"], ["quit"], ["exit"], []):
            with self.subTest(moves=moves):
                outcome, _ = play(Battleship(input_func=scripted_input(moves)))
                self.assertEqual(outcome, "quit")


if __name__ == "__main__":
    unittest.main()
