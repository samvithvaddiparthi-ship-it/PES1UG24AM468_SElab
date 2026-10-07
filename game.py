from board import Board
from ai import AI
from coords import parse_coord, format_coord

# Internal coordinates are 0-based: (1, 1) is shown to the player as 2,2.
PLAYER_FLEET = {
    "Cruiser": [(1, 1), (1, 2), (1, 3)],
    "Destroyer": [(3, 4), (4, 4)],
    "Patrol Boat": [(5, 0), (5, 1)],
}
ENEMY_FLEET = {
    "Cruiser": [(2, 2), (2, 3), (2, 4)],
    "Destroyer": [(4, 0), (5, 0)],
    "Patrol Boat": [(0, 4), (0, 5)],
}
QUIT_WORDS = {"q", "quit", "exit"}


class Battleship:
    def __init__(self, ai=None, input_func=input):
        self.player = Board()
        self.enemy = Board()
        self.ai = ai if ai is not None else AI()
        self.input = input_func
        self._setup()

    def _setup(self):
        for name, cells in PLAYER_FLEET.items():
            self.player.place_ship(name, cells)
        for name, cells in ENEMY_FLEET.items():
            self.enemy.place_ship(name, cells)

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print(f"Enemy ships afloat: {len(self.enemy.ships_afloat())}/{len(self.enemy.fleet)}"
              f" | Your ships afloat: {len(self.player.ships_afloat())}/{len(self.player.fleet)}")

    def _read_player_shot(self):
        """Prompt until the player gives a new, valid cell. None means quit."""
        while True:
            try:
                raw = self.input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if raw in QUIT_WORDS:
                return None
            try:
                pos = parse_coord(raw)
            except ValueError as err:
                print(err)
                continue
            if self.enemy.already_fired(pos):
                print(f"Already fired at {format_coord(pos)}. Pick another cell.")
                continue
            return pos

    def run(self):
        """Play until someone's fleet is sunk. Returns "player", "ai" or "quit"."""
        print("Battleship")
        while True:
            self.show()
            pos = self._read_player_shot()
            if pos is None:
                print("You quit the game.")
                return "quit"
            result = self.enemy.fire(pos)
            print("HIT!" if result.hit else "MISS!")
            if result.sunk_ship:
                print(f"You sank the enemy {result.sunk_ship.name}!")
            if self.enemy.all_sunk():
                print("You sank the fleet. You win!")
                return "player"

            ai_pos = self.ai.choose()
            result = self.player.fire(ai_pos)
            print("AI fired at", format_coord(ai_pos))
            print("AI scored a hit." if result.hit else "AI missed.")
            if result.sunk_ship:
                print(f"The AI sank your {result.sunk_ship.name}!")
            if self.player.all_sunk():
                print("The AI sank your whole fleet. You lose.")
                return "ai"
