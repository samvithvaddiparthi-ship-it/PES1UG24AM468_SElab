"""Task 3: AI targets nearby cells after a hit and never repeats a shot."""
import random
import unittest

from ai import AI
from board import Board
from game import ENEMY_FLEET, Battleship
from coords import format_coord
from tests.helpers import play, scripted_input


def neighbours(pos):
    r, c = pos
    return {(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)}


def take_shot(ai, board):
    pos = ai.choose()
    result = board.fire(pos)
    ai.record(pos, result)
    return pos, result


class AITests(unittest.TestCase):
    def test_never_repeats_and_covers_whole_board(self):
        for seed in range(20):
            ai = AI(rng=random.Random(seed))
            shots = [ai.choose() for _ in range(Board.SIZE * Board.SIZE)]
            self.assertEqual(len(set(shots)), Board.SIZE * Board.SIZE)

    def test_no_remaining_choices_returns_none(self):
        ai = AI(rng=random.Random(0))
        for _ in range(Board.SIZE * Board.SIZE):
            ai.choose()
        self.assertIsNone(ai.choose())
        self.assertIsNone(ai.choose())

    def test_tiny_board_with_no_choices(self):
        ai = AI(size=1)
        self.assertEqual(ai.choose(), (0, 0))
        self.assertIsNone(ai.choose())

    def test_targets_untried_neighbour_after_hit(self):
        for seed in range(20):
            board = Board()
            board.place_ship("Cruiser", [(2, 2), (2, 3), (2, 4)])
            ai = AI(rng=random.Random(seed))
            ai.tried.add((2, 2))
            ai.record((2, 2), board.fire((2, 2)))
            pos = ai.choose()
            self.assertIn(pos, neighbours((2, 2)))

    def test_skips_tried_and_off_board_neighbours(self):
        board = Board()
        board.place_ship("Patrol Boat", [(0, 0), (0, 1)])
        ai = AI(rng=random.Random(1))
        ai.tried.update({(0, 0), (1, 0)})
        ai.record((0, 0), board.fire((0, 0)))
        self.assertEqual(ai.choose(), (0, 1))  # only untried, on-board neighbour

    def test_follows_the_line_after_two_hits(self):
        for seed in range(20):
            board = Board()
            board.place_ship("Cruiser", [(2, 1), (2, 2), (2, 3)])
            ai = AI(rng=random.Random(seed))
            for cell in [(2, 2), (2, 3)]:
                ai.tried.add(cell)
                ai.record(cell, board.fire(cell))
            self.assertIn(ai.choose(), {(2, 1), (2, 4)})

    def test_returns_to_hunting_after_sinking(self):
        board = Board()
        board.place_ship("Patrol Boat", [(0, 0), (0, 1)])
        ai = AI(rng=random.Random(3))
        for cell in [(0, 0), (0, 1)]:
            ai.tried.add(cell)
            ai.record(cell, board.fire(cell))
        self.assertEqual(ai.open_hits, set())

    def test_sinks_a_whole_fleet_without_repeats(self):
        for seed in range(25):
            board = Board()
            for name, cells in ENEMY_FLEET.items():
                board.place_ship(name, cells)
            ai = AI(rng=random.Random(seed))
            shots = 0
            while not board.all_sunk():
                take_shot(ai, board)  # Board.fire raises on any repeat
                shots += 1
            self.assertLessEqual(shots, Board.SIZE * Board.SIZE)

    def test_targeting_beats_random_on_average(self):
        def average_shots(make_ai):
            total = 0
            for seed in range(200):
                board = Board()
                for name, cells in ENEMY_FLEET.items():
                    board.place_ship(name, cells)
                ai = make_ai(seed)
                while not board.all_sunk():
                    take_shot(ai, board)
                    total += 1
            return total / 200

        class RandomOnly(AI):
            def record(self, pos, result):
                self.tried.add(pos)

        smart = average_shots(lambda s: AI(rng=random.Random(s)))
        dumb = average_shots(lambda s: RandomOnly(rng=random.Random(s)))
        self.assertLess(smart, dumb)


class GameAITests(unittest.TestCase):
    def test_game_survives_ai_with_no_choices(self):
        class EmptyAI:
            def choose(self):
                return None

            def record(self, pos, result):
                raise AssertionError("record must not be called without a shot")

        moves = [format_coord(c) for cells in ENEMY_FLEET.values() for c in cells]
        game = Battleship(ai=EmptyAI(), input_func=scripted_input(moves))
        outcome, out = play(game)
        self.assertEqual(outcome, "player")
        self.assertIn("The AI has no cells left to fire at.", out)


if __name__ == "__main__":
    unittest.main()
