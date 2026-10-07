import random

from coords import SIZE


class AI:
    def __init__(self, size=SIZE):
        self.size = size
        self.tried = set()

    def choose(self):
        """Return an untried cell as a 0-based (row, col) tuple."""
        options = [(r, c) for r in range(self.size) for c in range(self.size)
                   if (r, c) not in self.tried]
        pos = random.choice(options)
        self.tried.add(pos)
        return pos
