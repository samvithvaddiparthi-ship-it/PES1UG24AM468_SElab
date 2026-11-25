# Lab 5: Static Code Analysis — Hospital Patient System

**Your file:** `hospital_patient_system.py`

Follow the lab handout for the full instructions.

## About the program

A hospital patient records and admission manager. It admits patients into specific wards, processes discharges, calculates dynamic treatment costs, and exports admission ledgers.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python hospital_patient_system.py
   ```
   It asks one question. Press Enter to use the default, then try a few inputs of your own. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint hospital_patient_system.py > pylint_report.txt
   bandit -r hospital_patient_system.py > bandit_report.txt
   flake8 hospital_patient_system.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `hospital_patient_system.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

---

## Submission

**Name:** Samvith Vaddiparthi &nbsp;|&nbsp; **SRN:** PES1UG24AM468 &nbsp;|&nbsp; **Section:** H

| File | Description |
|------|-------------|
| `hospital_patient_system.py` | Cleaned version: 19 documented issues fixed, and the program still does its job |
| `issues.md` | Issue table (19 issues, high and medium severity first) and which commit fixed each one |
| `reflection.md` | Answers to the reflection questions |
| `pylint_report_before.txt` / `pylint_report_after.txt` | 5.19/10 → **10.00/10** |
| `bandit_report_before.txt` / `bandit_report_after.txt` | 5 issues (2 High, 1 Medium, 2 Low) → **No issues identified** |
| `flake8_report_before.txt` / `flake8_report_after.txt` | 11 issues → **0** (an empty Flake8 report means no issues) |

### Commits (one per tool)

1. **Bandit:** shell injection, MD5, `eval`, `try/except/pass`, insecure random, and the hard-coded master key
2. **Pylint:** mutable default argument, naming, unused code, file handling, docstrings, `__main__` guard
3. **Flake8:** line lengths (PEP 8)

### How to run

```bash
pip install pylint bandit flake8
python hospital_patient_system.py
pylint hospital_patient_system.py > pylint_report.txt
bandit -r hospital_patient_system.py > bandit_report.txt
flake8 hospital_patient_system.py > flake8_report.txt
```

Note: this README's "It asks one question" line came with the assigned repo, but the given `hospital_patient_system.py`
never asks for input, so the program runs without any prompts.
