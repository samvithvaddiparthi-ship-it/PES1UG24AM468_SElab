"""
Lab 7 - Fuzz testing traffic_fine.py with Hypothesis

Name : Samvith Vaddiparthi
SRN  : PES1UG24AM468
Repo : L6_L7_27_traffic_fine

Three kinds of property tests are used for each of the three functions:

  1. "no crash"  - completely random text (or None) must never raise.
  2. "malformed" - input that is *shaped* like the real format (pieces joined
                   with '-', ',' or '/') must never raise and must give a
                   sensible result. Random text alone rarely produces these.
  3. "valid"     - correctly formatted input must give the correct answer,
                   so the fixes cannot "cheat" by rejecting everything.

Contract checked by the tests (what the hardened functions guarantee):
  parse_ticket_id(s) -> (PREFIX, year, serial) tuple, or None if s is invalid
  total_fines(s)     -> int between 0 and 10000,    or None if s is invalid
  speed_excess(s)    -> int percentage >= 0,        or None if s is invalid

Run:
    pytest test_traffic_fine.py
"""
import string

from hypothesis import given, settings, strategies as st

from traffic_fine import parse_ticket_id, total_fines, speed_excess

FUZZ = settings(max_examples=500, deadline=None)

# Building blocks for format-shaped (but often malformed) inputs
any_piece = st.text(max_size=8)
int_piece = st.integers(min_value=-10**6, max_value=10**6).map(str)
piece = any_piece | int_piece | st.just("") | st.just(" 7 ") | st.just("٣")


# ===========================================================================
# parse_ticket_id
# ===========================================================================

@FUZZ
@given(st.text() | st.none())
def test_parse_ticket_id_no_crash(s):
    try:
        result = parse_ticket_id(s)
    except Exception as e:
        assert False, f"parse_ticket_id crashed on {s!r} with {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, tuple) and len(result) == 3)


@FUZZ
@given(st.lists(piece, min_size=0, max_size=5).map("-".join))
def test_parse_ticket_id_malformed_no_crash(s):
    try:
        result = parse_ticket_id(s)
    except Exception as e:
        assert False, f"parse_ticket_id crashed on {s!r} with {type(e).__name__}: {e}"
    if result is not None:
        prefix, year, serial = result
        assert prefix.isalpha() and prefix.isupper()
        assert 1000 <= year <= 9999
        assert serial >= 0


@FUZZ
@given(
    prefix=st.text(alphabet=string.ascii_letters, min_size=1, max_size=5),
    year=st.integers(min_value=1000, max_value=9999),
    serial=st.text(alphabet=string.digits, min_size=1, max_size=10),
)
def test_parse_ticket_id_valid(prefix, year, serial):
    ticket = f"{prefix}-{year}-{serial}"
    assert parse_ticket_id(ticket) == (prefix.upper(), year, int(serial))


# ===========================================================================
# total_fines
# ===========================================================================

@FUZZ
@given(st.text() | st.none())
def test_total_fines_no_crash(s):
    try:
        result = total_fines(s)
    except Exception as e:
        assert False, f"total_fines crashed on {s!r} with {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, int) and 0 <= result <= 10000)


@FUZZ
@given(st.lists(piece, min_size=1, max_size=6).map(",".join))
def test_total_fines_malformed_in_range(s):
    try:
        result = total_fines(s)
    except Exception as e:
        assert False, f"total_fines crashed on {s!r} with {type(e).__name__}: {e}"
    # A total of fines can never be negative or exceed the 10000 cap
    assert result is None or 0 <= result <= 10000, f"total_fines({s!r}) = {result}"


@FUZZ
@given(st.lists(st.integers(min_value=-50000, max_value=50000), min_size=1, max_size=10))
def test_total_fines_never_negative(amounts):
    # Well-formed integer CSV, but amounts may be negative
    csv = ",".join(str(a) for a in amounts)
    try:
        result = total_fines(csv)
    except Exception as e:
        assert False, f"total_fines crashed on {csv!r} with {type(e).__name__}: {e}"
    assert result is None or 0 <= result <= 10000, f"total_fines({csv!r}) = {result}"
    if any(a < 0 for a in amounts):
        # a negative fine is not a real fine and must be rejected
        assert result is None, f"negative amount accepted: total_fines({csv!r}) = {result}"


@FUZZ
@given(st.lists(st.integers(min_value=0, max_value=50000), min_size=1, max_size=10))
def test_total_fines_valid(amounts):
    csv = ",".join(str(a) for a in amounts)
    assert total_fines(csv) == min(sum(amounts), 10000)


# ===========================================================================
# speed_excess
# ===========================================================================

@FUZZ
@given(st.text() | st.none())
def test_speed_excess_no_crash(s):
    try:
        result = speed_excess(s)
    except Exception as e:
        assert False, f"speed_excess crashed on {s!r} with {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, int) and result >= 0)


@FUZZ
@given(st.integers(min_value=-500, max_value=500), st.integers(min_value=-500, max_value=500))
def test_speed_excess_malformed_numbers(speed, limit):
    s = f"{speed}/{limit}"
    try:
        result = speed_excess(s)
    except Exception as e:
        assert False, f"speed_excess crashed on {s!r} with {type(e).__name__}: {e}"
    # "Percent over the limit" can never be negative
    assert result is None or result >= 0, f"speed_excess({s!r}) = {result}"


@FUZZ
@given(st.integers(min_value=0, max_value=400), st.integers(min_value=1, max_value=200))
def test_speed_excess_valid(speed, limit):
    expected = (speed - limit) * 100 // limit if speed > limit else 0
    assert speed_excess(f"{speed}/{limit}") == expected
