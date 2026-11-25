# L6_L7_27 — Traffic Fine Calculator

Lab 6: Code and Branch Coverage

## About

A small Python module that calculates speeding fines by road zone, decides licence actions from penalty points and totals a set of fines.

## Files

| File | Description |
|------|-------------|
| `traffic_fine.py` | The module under test |
| `test_traffic_fine.py` | Starter test file |

Refer to the lab handout for instructions.

---

## Submission

**Name:** Samvith Vaddiparthi &nbsp;|&nbsp; **SRN:** PES1UG24AM468 &nbsp;|&nbsp; **Section:** H

| File | Description |
|------|-------------|
| `CodeCoverageTest_PES1UG24AM468_traffic_fine.py` | 12 tests that execute every line (100% statement coverage) |
| `BranchCoverageTest_PES1UG24AM468_traffic_fine.py` | 50 tests that take every branch both ways, with boundary values (100% branch coverage) |
| `screenshots/code_coverage_report.png` | `coverage report -m` for the code coverage tests |
| `screenshots/code_tests_under_branch_coverage.png` | Code coverage tests run with `--branch` (98%, branch `38->40` missed) |
| `screenshots/branch_coverage_report.png` | `coverage report -m` for the branch coverage tests |
| `PES1UG24AM468_Lab6_Coverage_Report.pdf` | Coverage analysis report |

### Results (traffic_fine.py)

| Test suite | Tests | Statements | Branches | Coverage |
|---|---|---|---|---|
| Starter `test_traffic_fine.py` | 2 | 9/35 | – | 26% line / 21% branch |
| `CodeCoverageTest_...` | 12 | 35/35 | 25/26 | **100% line** |
| `BranchCoverageTest_...` | 50 | 35/35 | 26/26 | **100% branch** |

### How to run

```bash
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_PES1UG24AM468_traffic_fine.py
coverage report -m
coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM468_traffic_fine.py
coverage report -m
```
