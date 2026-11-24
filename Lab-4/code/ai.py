import random

from coords import SIZE, in_bounds

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


class AI:
    """Hunt/target AI.

    Hunt: with no unsunk hits, fire at a random untried cell.
    Target: after a hit, fire at untried cells next to it. Once two hits
    line up, keep extending that line before trying other neighbours.
    Cells are 0-based (row, col) tuples and every cell is tried at most once.
    """

    def __init__(self, size=SIZE, rng=None):
        self.size = size
        self.rng = rng if rng is not None else random.Random()
        self.tried = set()
        self.open_hits = set()  # hits on ships that are not sunk yet

    def choose(self):
        """Return an untried cell, or None if every cell has been tried."""
        options = self._line_targets() or self._neighbour_targets() or self._untried()
        if not options:
            return None
        pos = self.rng.choice(sorted(options))
        self.tried.add(pos)
        return pos

    def record(self, pos, result):
        """Learn from the outcome of the shot the AI just took."""
        self.tried.add(pos)
        if result.hit:
            self.open_hits.add(pos)
        if result.sunk_ship:
            self.open_hits -= result.sunk_ship.cells

    def _is_open(self, pos):
        return in_bounds(pos, self.size) and pos not in self.tried

    def _untried(self):
        return {(r, c) for r in range(self.size) for c in range(self.size)
                if (r, c) not in self.tried}

    def _neighbour_targets(self):
        return {(r + dr, c + dc) for r, c in self.open_hits for dr, dc in DIRECTIONS
                if self._is_open((r + dr, c + dc))}

    def _line_targets(self):
        """Open cells at either end of a run of two or more adjacent hits."""
        targets = set()
        for r, c in self.open_hits:
            for dr, dc in ((0, 1), (1, 0)):
                if (r + dr, c + dc) not in self.open_hits:
                    continue
                for step in (1, -1):
                    end = (r, c)
                    while end in self.open_hits:
                        end = (end[0] + dr * step, end[1] + dc * step)
                    if self._is_open(end):
                        targets.add(end)
        return targets
