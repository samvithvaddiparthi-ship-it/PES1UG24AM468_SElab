"""
Lab 6 - Branch coverage tests for traffic_fine.py

Name : Samvith Vaddiparthi
SRN  : PES1UG24AM468
Repo : L6_L7_27_traffic_fine

Goal: make every decision (if / elif / for) in traffic_fine.py evaluate
to BOTH True and False, and test the boundary values of every condition.

The line-coverage suite reached 100% lines but missed branch 38->40
(the case where the total is NOT above 10000). This suite covers it, plus
every boundary on either side of each comparison.

Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM468_traffic_fine.py
    coverage report -m
"""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# ---------------------------------------------------------------------------
# speeding_fine(speed, limit, zone)
#   Decision 1: speed <= limit          (True / False)
#   Decision 2: zone == "school"        (True / False)
#   Decision 3: zone == "highway"       (True / False)
#   Decision 4: excess > 40             (True / False)
#   Decision 5: excess > 20             (True / False)
# ---------------------------------------------------------------------------

# Decision 1 True: below the limit and exactly at the limit (boundary)
@pytest.mark.parametrize("speed, limit", [(50, 60), (60, 60), (0, 60)])
def test_not_speeding_returns_zero(speed, limit):
    assert speeding_fine(speed, limit, "city") == 0


# Decision 1 False + Decision 2..5 combinations.
# Each zone is tested in all three fine bands:
#   excess 1..20  -> base
#   excess 21..40 -> base * 2
#   excess 41+    -> base * 3
@pytest.mark.parametrize("zone, base", [
    ("school", 2000),   # Decision 2 True
    ("highway", 1000),  # Decision 2 False, Decision 3 True
    ("city", 500),      # Decision 2 False, Decision 3 False
    ("rural", 500),     # any other zone also falls into the else branch
])
@pytest.mark.parametrize("excess, multiplier", [
    (1, 1),    # just over the limit           -> Decision 4 False, Decision 5 False
    (20, 1),   # boundary: excess == 20        -> Decision 5 False
    (21, 2),   # boundary: excess == 21        -> Decision 5 True
    (40, 2),   # boundary: excess == 40        -> Decision 4 False, Decision 5 True
    (41, 3),   # boundary: excess == 41        -> Decision 4 True
    (75, 3),   # far over the limit            -> Decision 4 True
])
def test_speeding_fine_by_zone_and_excess(zone, base, excess, multiplier):
    limit = 60
    assert speeding_fine(limit + excess, limit, zone) == base * multiplier


# Zone matching is exact (case-sensitive), so "School" is a normal zone
def test_zone_name_is_case_sensitive():
    assert speeding_fine(70, 60, "School") == 500


# ---------------------------------------------------------------------------
# license_action(points, is_commercial, repeat_offender)
#   Decision 1: points >= 12            (True / False)
#   Decision 2: is_commercial           (True / False)  [inside Decision 1]
#   Decision 3: points >= 8             (True / False)
#   Decision 4: repeat_offender         (True / False)  [inside Decision 3]
#   Decision 5: points >= 4             (True / False)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("points, is_commercial, repeat_offender, expected", [
    # Decision 1 True
    (12, True,  False, "revoke"),   # boundary 12, commercial      -> D2 True
    (20, True,  True,  "revoke"),   # commercial overrides repeat
    (12, False, False, "suspend"),  # boundary 12, private         -> D2 False
    (15, False, True,  "suspend"),
    # Decision 1 False, Decision 3 True
    (11, False, True,  "suspend"),  # boundary 11, repeat offender -> D4 True
    (8,  True,  True,  "suspend"),  # boundary 8,  repeat offender
    (11, True,  False, "warning"),  # commercial alone does not matter below 12
    (8,  False, False, "warning"),  # boundary 8, first offence    -> D4 False
    # Decision 3 False, Decision 5 True
    (7,  False, True,  "notice"),   # boundary 7, repeat flag ignored
    (4,  True,  False, "notice"),   # boundary 4
    # Decision 5 False
    (3,  False, False, "none"),     # boundary 3
    (2,  False, False, "none"),     # starter case
    (0,  True,  True,  "none"),     # no points at all
])
def test_license_action_all_branches(points, is_commercial, repeat_offender, expected):
    assert license_action(points, is_commercial, repeat_offender) == expected


# ---------------------------------------------------------------------------
# total_penalty(fines)
#   Loop     : for fine in fines        (0 iterations / 1+ iterations)
#   Decision 1: fine < 0                (True / False)
#   Decision 2: total > 10000           (True / False)
# ---------------------------------------------------------------------------

# Loop runs zero times -> total stays 0 (Decision 2 False)
def test_total_penalty_empty_list_is_zero():
    assert total_penalty([]) == 0


# Normal sum below the cap -> Decision 1 False, Decision 2 False (branch 38->40)
def test_total_penalty_sum_below_cap():
    assert total_penalty([500, 1000, 2000]) == 3500


# A zero fine is allowed (boundary of fine < 0)
def test_total_penalty_zero_fine_allowed():
    assert total_penalty([0, 0]) == 0


# Boundary: exactly 10000 is NOT capped (Decision 2 False)
def test_total_penalty_exactly_10000_not_capped():
    assert total_penalty([4000, 6000]) == 10000


# Boundary: 10001 is capped to 10000 (Decision 2 True)
def test_total_penalty_just_over_cap():
    assert total_penalty([10000, 1]) == 10000


# Far above the cap -> capped (Decision 2 True)
def test_total_penalty_capped_at_10000():
    assert total_penalty([6000, 5000, 3000]) == 10000


# Decision 1 True on the first element
def test_total_penalty_negative_first_fine_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-1])


# Decision 1 True after some valid fines (loop already iterated)
def test_total_penalty_negative_later_fine_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, 1000, -100])


# Works with any iterable, e.g. a tuple
def test_total_penalty_accepts_tuple():
    assert total_penalty((200, 300)) == 500
