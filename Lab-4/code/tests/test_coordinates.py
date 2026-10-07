"""Task 1: one coordinate representation across input, placement and shots."""
import unittest

from ai import AI
from board import Board
from coords import format_coord, parse_coord
from game import Battleship


class CoordinateTests(unittest.TestCase):
    def test_parse_is_one_based_text_to_zero_based_tuple(self):
        self.assertEqual(parse_coord("1,1"), (0, 0))
        self.assertEqual(parse_coord("2,3"), (1, 2))
        self.assertEqual(parse_coord(" 6 , 6 "), (5, 5))

    def test_format_round_trips(self):
        for r in range(Board.SIZE):
            for c in range(Board.SIZE):
                self.assertEqual(parse_coord(format_coord((r, c))), (r, c))

    def test_invalid_coordinates_rejected(self):
        for raw in ["", "2", "2,", ",3", "a,b", "1,2,3", "0,1", "1,0", "7,1", "1,7", "-1,2", "2.5,1"]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    parse_coord(raw)

    def test_ai_returns_internal_tuple(self):
        pos = AI().choose()
        self.assertIsInstance(pos, tuple)
        self.assertTrue(0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE)

    def test_every_ship_cell_hits_and_every_empty_cell_misses(self):
        # Both boards, every cell, exactly as the game sets them up.
        game = Battleship()
        for board in (game.player, game.enemy):
            ships = set(board.ships)
            for r in range(Board.SIZE):
                for c in range(Board.SIZE):
                    self.assertEqual(board.fire((r, c)).hit, (r, c) in ships)

    def test_player_text_hits_the_cell_it_names(self):
        game = Battleship()
        self.assertTrue(game.enemy.fire(parse_coord("3,3")).hit)   # enemy ship at (2, 2)
        self.assertFalse(game.enemy.fire(parse_coord("1,1")).hit)  # known empty cell

    def test_ai_shot_is_resolved_on_the_cell_it_chose(self):
        # Previously the AI's 1-based text was compared with 0-based cells,
        # so AI cell (0, 0) was reported as a hit on the ship at (1, 1).
        game = Battleship()
        self.assertFalse(game.player.fire((0, 0)).hit)
        self.assertTrue(game.player.fire((1, 1)).hit)
        self.assertEqual(game.player.shots, {(0, 0), (1, 1)})


if __name__ == "__main__":
    unittest.main()
