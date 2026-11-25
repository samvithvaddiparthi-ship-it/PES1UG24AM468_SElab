"""
Lab 6 - Code (line/statement) coverage tests for traffic_fine.py

Name : Samvith Vaddiparthi
SRN  : PES1UG24AM468
Repo : L6_L7_27_traffic_fine

Goal: make every line of traffic_fine.py execute at least once.

Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM468_traffic_fine.py
    coverage report -m
"""
import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# ---------------------------------------------------------------------------
# speeding_fine(speed, limit, zone)
# ---------------------------------------------------------------------------

# Starter test: speed within the limit -> no fine (line 3)
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


# School zone base fine (line 6) + excess > 40 -> base * 3 (line 12)
def test_school_zone_excess_over_40():
    # excess = 105 - 60 = 45
    assert speeding_fine(105, 60, "school") == 2000 * 3


# Highway zone base fine (line 8) + excess > 20 -> base * 2 (line 14)
def test_highway_zone_excess_over_20():
    # excess = 130 - 100 = 30
    assert speeding_fine(130, 100, "highway") == 1000 * 2


# Any other zone base fine (line 10) + small excess -> base only (line 15)
def test_city_zone_small_excess():
    # excess = 70 - 60 = 10
    assert speeding_fine(70, 60, "city") == 500


# ---------------------------------------------------------------------------
# license_action(points, is_commercial, repeat_offender)
# ---------------------------------------------------------------------------

# Starter test: few points -> "none" (line 29)
def test_clean_record():
    assert license_action(2, False, False) == "none"


# 12+ points and commercial driver -> "revoke" (line 21)
def test_commercial_driver_high_points_revoked():
    assert license_action(12, True, False) == "revoke"


# 12+ points and private driver -> "suspend" (line 22)
def test_private_driver_high_points_suspended():
    assert license_action(15, False, False) == "suspend"


# 8-11 points and repeat offender -> "suspend" (line 25)
def test_repeat_offender_medium_points_suspended():
    assert license_action(9, False, True) == "suspend"


# 8-11 points, first offence -> "warning" (line 26)
def test_first_offender_medium_points_warning():
    assert license_action(8, False, False) == "warning"


# 4-7 points -> "notice" (line 28)
def test_low_points_notice():
    assert license_action(5, False, False) == "notice"


# ---------------------------------------------------------------------------
# total_penalty(fines)
# ---------------------------------------------------------------------------

# Total above 10000 is capped at 10000 (lines 33-37, 38-40)
def test_total_penalty_capped_at_10000():
    assert total_penalty([6000, 5000]) == 10000


# A negative fine raises ValueError (line 36)
def test_total_penalty_negative_fine_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, -100])
