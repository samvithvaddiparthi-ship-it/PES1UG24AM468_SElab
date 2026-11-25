"""Single source of truth for coordinates.

Inside the game every coordinate is a 0-based ``(row, col)`` tuple: ship
placement, the shots stored on a board, player shots and AI shots all use
it. The 1-based ``"row,col"`` text the player types and reads is converted
only at the edges with :func:`parse_coord` and :func:`format_coord`.
"""

SIZE = 6


def in_bounds(pos, size=SIZE):
    row, col = pos
    return 0 <= row < size and 0 <= col < size


def parse_coord(raw, size=SIZE):
    """Convert player text such as ``"2,3"`` into the internal ``(1, 2)``.

    Raises ValueError with a message that can be shown to the player.
    """
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError("Use row,col (for example 2,3).")
    try:
        row, col = (int(part) for part in parts)
    except ValueError:
        raise ValueError("Use row,col (for example 2,3).") from None
    pos = (row - 1, col - 1)
    if not in_bounds(pos, size):
        raise ValueError(f"Outside board. Rows and columns go from 1 to {size}.")
    return pos


def format_coord(pos):
    """Convert an internal ``(row, col)`` tuple into the text the player sees."""
    return f"{pos[0] + 1},{pos[1] + 1}"
