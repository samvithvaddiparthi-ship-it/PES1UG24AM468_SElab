from board import Board
from ai import AI
from coords import parse_coord, format_coord


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Internal coordinates are 0-based: (1, 1) is shown to the player as 2,2.
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Ship cells remaining:", self.enemy.remaining())

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            try:
                pos = parse_coord(raw)
            except ValueError as err:
                print(err)
                continue
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue
            print("HIT!" if self.enemy.fire(pos) else "MISS!")
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            # The AI hands back the same (row, col) tuple used everywhere
            # else, and its shot is resolved against the player's board.
            ai_pos = self.ai.choose()
            print("AI fired at", format_coord(ai_pos))
            print("AI scored a hit." if self.player.fire(ai_pos) else "AI missed.")
