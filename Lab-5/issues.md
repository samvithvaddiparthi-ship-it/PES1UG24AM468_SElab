# Lab 5 – Static Code Analysis: Issue Table

**Name:** Samvith Vaddiparthi &nbsp;|&nbsp; **SRN:** PES1UG24AM468 &nbsp;|&nbsp; **Section:** H
**Assigned repo:** [SETAPESU26/L5_46_hospital_patient_management_system](https://github.com/SETAPESU26/L5_46_hospital_patient_management_system) &nbsp;|&nbsp; **File:** `hospital_patient_system.py`

Tools: Pylint 4.1.4, Bandit 1.9.4, Flake8 7.5.0 (Python 3.12).
Line numbers refer to the **original** file (see `*_report_before.txt`).

## Baseline (before fixes)

| Tool | Result |
|------|--------|
| Pylint | **5.19/10**, 26 messages |
| Bandit | **5 issues**: 2 High, 1 Medium, 2 Low |
| Flake8 | **11 issues** |

## Issues found (high and medium severity first)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Shell command injection | Security – Bandit **B605 (High)** | 56 | `os.system("echo ... " + filename)` passes the file name to a shell. A name like `x.txt; rm -rf ~` would run any command. | Removed the shell call; print the message with `print()`. `import os` is no longer needed. |
| 2 | Weak MD5 hash | Security – Bandit **B324 (High)** | 45 | MD5 is broken (collisions are cheap to produce) and should not be used to hash patient IDs. | Use `hashlib.sha256`. |
| 3 | Hard-coded master key printed to the console | Security – **not flagged by any tool** | 68, 77 | `nurse_access_key = "HOSPITAL_NURSE_MASTER_KEY_2026"` is stored in the source code and printed on every run. Bandit's B105 check missed it because of the variable name. | Removed the secret from the code and the output. A real key belongs in an environment variable or a secret store, never in source. |
| 4 | `eval()` on a formula string | Security – Bandit **B307 (Medium)**, Pylint W0123 | 39–40 | `eval(formula_expr)` runs any Python expression it is given (arbitrary code execution). It also hides the use of `base_bill`, so tools report it as unused. | Replaced the string formula with a numeric `multiplier` parameter (default 1.12), validated as a non-negative number: `base_bill * multiplier`. |
| 5 | Mutable default argument | Bug – Pylint **W0102** | 13, 17 | `intake_log=[]` is created once and shared by every call. Admitting P201 and then P202 leaves both entries in the same default list. | Default to `None` and create a new list inside the function. |
| 6 | Errors silently swallowed (`try/except: pass`) | Bug – Bandit B110 (Low), Pylint W0702, Flake8 E722 | 22–25 | A bare `except: pass` hides every error. Discharging an unknown ID such as `"P999"` does nothing and the caller cannot tell. | Check `p_id in patient_records`, return `True`/`False`, and remove the try/except. |
| 7 | Floating-point money shown to the user | Bug – **not flagged by any tool** | 40, 72 | The program prints `Cost calculated: 1344.0000000000002` (1200 × 1.12 in binary floating point). | Round the cost to 2 decimal places: `round(total, 2)` → `1344.0`. |
| 8 | Predictable random token | Security – Bandit B311 (Low) | 49 | `random.randint` is not cryptographically secure, so ward tokens can be predicted. | Use `secrets.randbelow(9000) + 1000` (still 1000–9999). |
| 9 | File opened without `with` / encoding | Convention – Pylint R1732, W1514 | 53–55 | The file is not closed if `write` fails, and the encoding depends on the platform. The ledger is written as `str(dict)`, which is hard to read back. | `with open(filename, "w", encoding="utf-8")` and write the records as indented JSON. |
| 10 | `main()` runs on import | Design – **not flagged by any tool** | 80 | Importing the module (e.g. from a test) admits and discharges patients and writes a file. | Wrap in `if __name__ == "__main__":`. |
| 11 | Unused import and variables | Warning – Pylint W0611/W0612, Flake8 F401/F841 | 4, 29, 39, 61 | `math`, `bed_charge`, `base_bill` (after `eval`) and loop variable `p` are dead code. | Removed them. Loop over `.values()`. |
| 12 | Parameter shadows global | Warning – Pylint W0621 | 59 | `get_ward_summary(patient_records)` hides the module-level `patient_records`. | Renamed the parameter to `records`. |
| 13 | Non-snake_case function name | Convention – Pylint C0103 | 13, 69 | `admitPatient` breaks PEP 8 naming. | Renamed to `admit_patient` and updated the call. |
| 14 | `== None` comparison | Convention – Pylint C0121, Flake8 E711 | 30 | Comparing to `None` should use identity. | Rewritten as `record is not None and record["is_admitted"]`. |
| 15 | Over-complicated `if/else` return | Refactor – Pylint R1703, R1705 | 32–35 | `if x: return True else: return False`. | Return the boolean expression directly. |
| 16 | Old `%` string formatting | Convention – Pylint C0209 | 17 | `"..." % (...)`. | f-string. |
| 17 | Missing docstrings | Convention – Pylint C0114, C0116 | 1, 13, 21, 28, 38, 44, 48, 52, 59, 67 | No module or function documentation. | Added a module docstring and a docstring to every function. |
| 18 | Lines too long | Style – Flake8 E501 | 7, 8, 9, 16, 72 | Lines are 83–93 characters (PEP 8 limit is 79). | Wrapped the dictionaries and long calls over several lines. |
| 19 | No newline at end of file | Style – Pylint C0304, Flake8 W292 | 80 | The file does not end with a newline. | Added the final newline. |

## Which commit fixes what

| Commit | Tool | Issues fixed |
|--------|------|--------------|
| 1 | Bandit (security) | #1, #2, #3, #4, #6, #7, #8 |
| 2 | Pylint (quality) | #5, #9, #10, #11, #12, #13, #14, #15, #16, #17, #19 |
| 3 | Flake8 (style) | #18 |
