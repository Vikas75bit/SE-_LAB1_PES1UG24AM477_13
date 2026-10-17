# Static Code Analysis: Issues, Vulnerabilities, and Fixes

This document details the issues identified during static code analysis of `pharmacy_manager.py` using **Bandit**, **Pylint**, and **Flake8**, along with their root causes, remediation strategies, and verification outcomes.

---

## Summary of Analysis Results

| Analysis Tool | Baseline (Before) | Final (After) | Status |
|---|---|---|---|
| **Bandit** (Security) | 8 issues (2 High, 2 Medium, 4 Low) | **0 issues** | Fully Resolved |
| **Pylint** (Code Quality) | **4.83 / 10** | **10.00 / 10** (+5.17) | Fully Resolved |
| **Flake8** (PEP 8 Style) | 22 violations | **0 violations** | Fully Resolved |

---

## Detailed Issue Tracking Table

| Issue | Tool & Rule | Type / Severity | Line(s)* | Description & Root Cause | Fix Approach | Verification Status |
|---|---|---|---:|---|---|---|
| **Shell Command Injection** | Bandit `B605` | Security — High | 68 | `os.system("echo Dispensing label: " + name)` concatenates unsanitized input into an OS shell command, enabling arbitrary command execution. | Removed `os.system()` shell execution entirely; replaced with Python native `print()` formatting. | **Verified Fixed** (Bandit: clean) |
| **Weak Hash for Patient ID** | Bandit `B324` | Security — High | 51 | `hashlib.md5()` uses MD5, which is cryptographically broken with known collision and pre-image attacks. | Replaced with `hashlib.sha256()`. (Note: while hashing improves collision resistance, true patient anonymity requires proper de-identification/salting). | **Verified Fixed** (Bandit: clean) |
| **Arbitrary Code Execution via `eval()`** | Bandit `B307` / Pylint `W0123` | Security — Medium | 48 | `calculateDosage(formula)` used Python's built-in `eval()` on user-supplied strings, allowing arbitrary code execution. | Replaced `eval()` with a restricted recursive AST parser using `ast.parse(mode="eval")` that only evaluates numeric literals and basic binary operations (`+`, `-`, `*`, `/`). | **Verified Fixed** (Bandit & Pylint: clean) |
| **Unsafe Deserialization via `pickle`** | Bandit `B301`, `B403` | Security — Medium | 3, 64 | `pickle.load()` deserializes arbitrary Python objects from disk, which can trigger arbitrary code execution via forged pickle payloads. | Replaced `pickle` with standard `json` format (`json.dump` / `json.load`) and added schema validation on the loaded stock dictionary. | **Verified Fixed** (Bandit: clean) |
| **Hardcoded Password Credential** | Bandit `B105` | Security — Low | 11 | `DB_PASSWORD = "pharma@123"` stores plaintext credentials directly in source control. | Replaced hardcoded string with environment variable lookup via `os.environ.get("PHARMACY_PASSWORD", ...)` to allow secure runtime configuration. | **Verified Fixed** (Bandit: clean) |
| **Predictable Prescription Numbers** | Bandit `B311` | Security — Low | 54 | `random.randint()` uses the Mersenne Twister pseudo-random number generator, which is predictable and unsuitable for security-sensitive tokens. | Replaced `random` with the cryptographically secure `secrets` module (`secrets.randbelow(900000) + 100000`). | **Verified Fixed** (Bandit: clean) |
| **Bare Exception Handling** | Bandit `B110` / Pylint `W0702` / Flake8 `E722` | Code Quality / Security | 27–28 | `try: ... except: pass` in `dispenseMedicine` catches all exceptions including system exits, silently ignoring errors and masking bugs. | Removed bare `except: pass`; added explicit conditional logic and validation to verify medicine existence and available stock quantity. | **Verified Fixed** (Bandit, Pylint, Flake8: clean) |
| **Mutable Default Argument** | Pylint `W0102` | Code Quality — Warning | 13 | `addMedicine(..., audit=[])` uses a mutable list default, which is shared across all function calls throughout the runtime process. | Changed default parameter to `audit=None` and initialized `audit = []` inside the function body when `None`. | **Verified Fixed** (Pylint: clean) |
| **Inconsistent Return Statements** | Pylint `R1710` | Code Quality — Refactor | 13, 17 | `addMedicine` returned `None` implicitly on early exit when `not name`, but returned `audit` on success. | Updated all execution paths to return explicit values (`None` on validation error, `audit` on success). | **Verified Fixed** (Pylint: clean) |
| **Unchecked Inventory Logic Defects** | Manual Inspection & Runtime Audit | Logic Bug | 16–20, 92–95 | `addMedicine` allowed negative quantities (e.g. `-10`) and non-string medicine names (e.g. `404`). `dispenseMedicine` allowed dispensing non-existent medicines or exceeding available stock without warning. | Added strict type checks (`isinstance(name, str)`), non-negative quantity and price checks, date validation, and explicit stock sufficiency checks before decrementing. | **Verified Fixed** (Runtime tests pass, invalid actions rejected cleanly) |
| **Unmanaged File Handles** | Pylint `R1732` | Code Quality — Refactor | 57, 62 | `saveStock` and `loadStock` opened files with `f = open(...)` without ensuring resource release on exceptions. | Replaced manual file operations with `with open(..., encoding="utf-8") as ...` context managers. | **Verified Fixed** (Pylint: clean) |
| **Unused Imports** | Pylint `W0611` / Flake8 `F401` | Code Quality / Style | 2, 6 | `sys` and `logging` were imported but never referenced in the module. | Removed unused `sys` and `logging` imports. | **Verified Fixed** (Pylint & Flake8: clean) |
| **Missing Module & Function Docstrings** | Pylint `C0114`, `C0116` | Code Quality — Convention | 1, 13–89 | Neither the module nor any of its functions had docstrings explaining purpose, parameters, or return values. | Added comprehensive PEP 257 docstrings for the module and all functions. | **Verified Fixed** (Pylint: clean) |
| **Non-Standard Naming Conventions** | Pylint `C0103` | Code Quality — Convention | 13–84 | Functions used `camelCase` (e.g., `addMedicine`, `dispenseMedicine`, `billAmount`) violating PEP 8 snake_case standards. | Renamed all functions to snake_case (`add_medicine`, `dispense_medicine`, `bill_amount`, etc.) and updated all call sites. | **Verified Fixed** (Pylint: clean) |
| **Simplifiable Conditionals** | Pylint `R1703`, `R1705` | Code Quality — Refactor | 35–40, 79–84 | `if cond: return True else: return False` used redundant branching and unnecessary `else` blocks. | Replaced with direct boolean expressions: `return exp < date.today()` and `return password == DB_PASSWORD`. | **Verified Fixed** (Pylint: clean) |
| **Blank Line Violations** | Flake8 `E302`, `E305` | Style Violation | 13–108 | Functions and top-level statements were separated by only 1 blank line instead of PEP 8's required 2 blank lines. | Added standard 2 blank lines before all top-level functions and before the `if __name__ == "__main__":` entry point. | **Verified Fixed** (Flake8: clean) |
| **Excessive Line Lengths** | Flake8 `E501` / Pylint `C0301` | Style Violation | 19, 87, 98 | Lines exceeded 79 characters (up to 111 characters in stock printing and string formatting). | Re-wrapped statements, multiline function arguments, and f-strings to strictly comply with the 79-character limit. | **Verified Fixed** (Flake8 & Pylint: clean) |

*\* Note: Line numbers refer to the baseline file `pharmacy_manager.py` (commit `18faab2`).*