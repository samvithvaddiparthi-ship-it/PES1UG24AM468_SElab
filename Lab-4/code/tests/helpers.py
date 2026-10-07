"""Shared test helpers: scripted input and a scripted AI."""
import contextlib
import io


class ScriptedAI:
    """Stands in for AI; fires at a fixed list of 0-based cells in order."""

    def __init__(self, shots):
        self.shots = list(shots)
        self.recorded = []

    def choose(self):
        return self.shots.pop(0) if self.shots else None

    def record(self, pos, result):
        self.recorded.append((pos, result))


def scripted_input(lines):
    """input() replacement that replays lines, then behaves like Ctrl+D."""
    lines = list(lines)

    def fake_input(prompt=""):
        if not lines:
            raise EOFError
        return lines.pop(0)
    return fake_input


def play(game):
    """Run a game, returning (outcome, printed output)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        outcome = game.run()
    return outcome, out.getvalue()
