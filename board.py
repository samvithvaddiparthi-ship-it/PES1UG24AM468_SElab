from coords import SIZE, in_bounds


class Board:
    SIZE = SIZE

    def __init__(self, size=SIZE):
        self.size = size
        self.ships = set()  # occupied cells, 0-based (row, col)
        self.shots = set()  # cells fired at on this board, 0-based (row, col)

    def place_ship(self, cells):
        cells = set(cells)
        if not all(in_bounds(cell, self.size) for cell in cells):
            raise ValueError("Ship placed outside the board.")
        self.ships.update(cells)

    def fire(self, pos):
        self.shots.add(pos)
        return pos in self.ships

    def remaining(self):
        return len(self.ships - self.shots)

    def all_sunk(self):
        return self.ships <= self.shots
