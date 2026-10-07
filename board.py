from coords import SIZE, format_coord, in_bounds


class RepeatedShotError(ValueError):
    """Raised when a cell that was already fired at is fired at again."""


class Ship:
    def __init__(self, name, cells):
        self.name = name
        self.cells = frozenset(cells)
        self.hits = set()

    @property
    def sunk(self):
        return self.hits == self.cells


class ShotResult:
    """Outcome of one shot: whether it hit and which ship (if any) it sank."""

    def __init__(self, pos, hit, sunk_ship=None):
        self.pos = pos
        self.hit = hit
        self.sunk_ship = sunk_ship


class Board:
    SIZE = SIZE

    def __init__(self, size=SIZE):
        self.size = size
        self.fleet = []
        self.shots = set()  # cells fired at on this board, 0-based (row, col)

    @property
    def ships(self):
        """Every occupied cell, 0-based (row, col)."""
        return {cell for ship in self.fleet for cell in ship.cells}

    def place_ship(self, name, cells):
        cells = set(cells)
        if not cells:
            raise ValueError("A ship needs at least one cell.")
        if not all(in_bounds(cell, self.size) for cell in cells):
            raise ValueError(f"{name} is outside the board.")
        if cells & self.ships:
            raise ValueError(f"{name} overlaps another ship.")
        rows = {r for r, _ in cells}
        cols = {c for _, c in cells}
        straight = len(rows) == 1 or len(cols) == 1
        line = cols if len(rows) == 1 else rows
        unbroken = max(line) - min(line) + 1 == len(cells)
        if not (straight and unbroken):
            raise ValueError(f"{name} must be one straight, unbroken line.")
        ship = Ship(name, cells)
        self.fleet.append(ship)
        return ship

    def ship_at(self, pos):
        for ship in self.fleet:
            if pos in ship.cells:
                return ship
        return None

    def already_fired(self, pos):
        return pos in self.shots

    def fire(self, pos):
        if not in_bounds(pos, self.size):
            raise ValueError("Shot outside the board.")
        if pos in self.shots:
            raise RepeatedShotError(f"Already fired at {format_coord(pos)}.")
        self.shots.add(pos)
        ship = self.ship_at(pos)
        if ship is None:
            return ShotResult(pos, hit=False)
        ship.hits.add(pos)
        return ShotResult(pos, hit=True, sunk_ship=ship if ship.sunk else None)

    def remaining(self):
        return len(self.ships - self.shots)

    def ships_afloat(self):
        return [ship for ship in self.fleet if not ship.sunk]

    def all_sunk(self):
        return bool(self.fleet) and all(ship.sunk for ship in self.fleet)
