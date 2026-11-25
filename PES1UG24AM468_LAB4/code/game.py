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
        """Draw both boards side by side with the fleet status."""
        enemy_rows = self.enemy.render(reveal_ships=False)
        player_rows = self.player.render(reveal_ships=True)
        width = len(enemy_rows[0])
        print()
        print(f"{'ENEMY WATERS':<{width}}    YOUR FLEET")
        for left, right in zip(enemy_rows, player_rows):
            print(f"{left}    {right}")
        print(f"Enemy ships afloat: {len(self.enemy.ships_afloat())}/{len(self.enemy.fleet)}"
              f" | Your ships afloat: {len(self.player.ships_afloat())}/{len(self.player.fleet)}")
        print("X hit  o miss  # sunk  S your ship | shoot with row,col e.g. 2,3 | q quits")

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

    @staticmethod
    def shot_message(shooter, result):
        """The one feedback line for one actual shot."""
        message = f"{shooter} fire{'s' if shooter == 'AI' else ''} at {format_coord(result.pos)}: "
        if not result.hit:
            return message + "miss."
        message += "HIT!"
        if result.sunk_ship:
            owner = "the enemy" if shooter == "You" else "your"
            message += f" {shooter} sank {owner} {result.sunk_ship.name}!"
        return message

    def _take_shot(self, shooter, board, pos):
        """Resolve one real shot and announce it exactly once."""
        result = board.fire(pos)
        print(self.shot_message(shooter, result))
        return result

    def run(self):
        """Play until someone's fleet is sunk. Returns "player", "ai" or "quit"."""
        print("Battleship - sink the enemy fleet before the AI sinks yours.")
        while True:
            self.show()
            pos = self._read_player_shot()
            if pos is None:
                print("You quit the game.")
                return "quit"
            self._take_shot("You", self.enemy, pos)
            if self.enemy.all_sunk():
                self.show()
                print("You sank the whole enemy fleet. You win!")
                return "player"

            # Choosing a target is silent; only the shot itself is announced.
            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("The AI has no cells left to fire at.")
                continue
            self.ai.record(ai_pos, self._take_shot("AI", self.player, ai_pos))
            if self.player.all_sunk():
                self.show()
                print("The AI sank your whole fleet. You lose.")
                return "ai"
