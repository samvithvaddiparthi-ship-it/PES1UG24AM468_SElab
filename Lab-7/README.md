# L6_L7_27 — Traffic Fine Calculator

Lab 7: Fuzz Testing

## About

A small Python module that parses traffic ticket details, totals fines and measures how far over the limit a driver was.

## Files

| File | Description |
|------|-------------|
| `traffic_fine.py` | The code under test |
| `test_traffic_fine.py` | Starter test file |

Refer to the lab handout for instructions.

---

## Submission

**Name:** Samvith Vaddiparthi &nbsp;|&nbsp; **SRN:** PES1UG24AM468 &nbsp;|&nbsp; **Section:** H

| File | Description |
|------|-------------|
| `traffic_fine.py` | **Fixed** application: invalid input returns `None` instead of crashing |
| `test_traffic_fine.py` | Completed Hypothesis fuzz tests (10 property tests, 500 examples each) |
| `screenshots/step2_buggy_run_*.png` | Buggy program crashing on `TF2024`, `500,,300`, `72/0` |
| `screenshots/step4_tests_failing_*of7.png` | Fuzz tests on the buggy code: 8 failed, 2 passed |
| `screenshots/step5_fixed_run_*.png` | Fixed program handling the same inputs |
| `screenshots/step6_tests_passing.png` | Fuzz tests on the fixed code: 10 passed |
| `PES1UG24AM468_Lab7_FuzzTesting_Report.pdf` | Report with all screenshots, the 13 bugs found and the fixes |

### Bugs found by Hypothesis (minimal inputs)

| Function | Inputs | Original behaviour |
|---|---|---|
| `parse_ticket_id` | `None`, `''`, `'--'` | AttributeError / ValueError crash |
| `parse_ticket_id` | `'-0- 7 '` | accepted with an empty prefix: `('', 0, 7)` |
| `total_fines` | `None`, `''` | AttributeError / ValueError crash |
| `total_fines` | `'-1'`, `'1,-1'` | negative or wrong total (`-1`, `0`) |
| `speed_excess` | `None`, `''`, `'/'` | AttributeError / ValueError crash |
| `speed_excess` | `'0/0'` | ZeroDivisionError |
| `speed_excess` | `'0/1'` | negative percentage (`-100`) |

### How to run

```bash
pip install hypothesis pytest
python traffic_fine.py
pytest test_traffic_fine.py
```
