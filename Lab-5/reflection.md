# Lab 5 – Reflection

**Name:** Samvith Vaddiparthi &nbsp;|&nbsp; **SRN:** PES1UG24AM468 &nbsp;|&nbsp; **Section:** H

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.19/10 (26 messages) | **10.00/10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **No issues identified** |
| Flake8 | 11 issues | **0 issues** |

> The handout asks for answers to the lab's reflection questions but does not list them, so I answered the four standard questions for this lab.

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the style and convention issues: unused `import math`, unused variables, the missing final newline,
`== None` → `is None`, renaming `admitPatient` to `admit_patient`, and wrapping long lines. Each warning names the
exact line and rule, and the fix is mechanical, with no effect on behaviour.

**Hardest:** the `eval(formula_expr)` call (Bandit B307). Deleting `eval` is easy, but the function still has to compute
a cost. I had to decide what callers really need. The only use was `"base_bill * 1.12"`, so I replaced the free-form
formula with a validated numeric `multiplier` parameter. That changes the function's interface, so the call in `main()`
had to change too. The mutable default argument (`intake_log=[]`) also needed thought: Pylint only says it is
"dangerous". I had to show the real bug (admitting two patients leaves both entries in the same shared list) and decide
how the log should be passed back to callers.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no real false positives, but some findings were weaker than their severity suggests, and the tools missed some
things entirely:

- **Overstated:** Bandit B311 (`random.randint` for the ward token) only matters if the token is used for access control.
  For a display number it would be a false positive. Since a "ward token" sounds like an access code, I still switched to
  `secrets`.
- **Duplicates:** several problems were reported by two or three tools at once (bare `except` by Bandit B110, Pylint
  W0702 and Flake8 E722; unused variables by both Pylint and Flake8), which inflates the raw issue count.
- **Misleading:** Pylint reported `base_bill` as an unused variable. It *was* used, but only inside the `eval` string,
  which static analysis cannot see.
- **Missed (false negatives):** none of the tools flagged the hard-coded `nurse_access_key` that was **printed on every
  run**, which was the most serious leak in the program. None of them flagged the money value printed as
  `1344.0000000000002`, discharges of unknown patients silently doing nothing, or `main()` running on import. I found
  these by running the program and reading the code. Static analysis complements code review and testing; it doesn't
  replace them.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **In the editor:** run Pylint and Flake8 as linters in VS Code so problems show up while typing.
- **Pre-commit hook:** use the `pre-commit` framework to run `flake8`, `pylint --fail-under=9.5` and `bandit -ll` before
  every commit, so bad code never reaches the repository.
- **CI pipeline:** run all three tools in GitHub Actions on every push and pull request, and block merging if Bandit finds
  a Medium/High issue or the Pylint score drops below the threshold. This fits the CI/CD project for this course.
- **Shared configuration:** keep the settings in `pyproject.toml` / `.flake8` (line length, disabled checks) so everyone
  on the team gets the same results, and use `# nosec` / `# pylint: disable` only with a written reason.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** no shell command built from user data, no `eval`, SHA-256 instead of MD5, a secure random token, and the
  master key is no longer in the code or the output.
- **Correctness:** admissions no longer share a hidden log list. Discharging an unknown patient returns `False`
  instead of failing silently. Costs print as `1344.0` instead of `1344.0000000000002`. Invalid multipliers raise a
  clear `ValueError`.
- **Robustness:** the ledger is written with a context manager and an explicit UTF-8 encoding, as JSON that can be read
  back, and importing the module no longer runs `main()`. That made the module easy to test: I imported it and
  checked every function.
- **Readability:** every function has a docstring and a PEP 8 name, and the simpler logic
  (`return record is not None and record["is_admitted"]`, `sum(...)` instead of a counter loop) makes the file shorter
  and clearer. The Pylint score went from 5.19 to 10.00/10.
