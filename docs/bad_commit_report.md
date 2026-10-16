# Scenario 5: Undoing a Bad Commit

## 1. Executive Summary
During feature development, a breaking commit was introduced that caused critical service failures. Rather than destroying commit history using destructive commands like `git reset`, the issue was isolated, reproduced, and safely rolled back using `git revert`. The fix was verified using automated unit testing (`pytest`).

---

## 2. Step-by-Step Execution

### Step 1: Branch Creation & Issue Reproduction
A temporary feature branch was created from the working state:
```bash
git switch -c feature/scenario-bad-commit
```

A breaking bug (division by zero) was introduced into the `/health` endpoint inside `main.py`:
```python
@app.get("/health")
def health_check():
    return 1 / 0  # ZeroDivisionError breaks the endpoint
```

The faulty change was committed to local history:
```bash
git add main.py
git commit -m "wip: accidental bad commit that breaks health check"
```

### Step 2: Automated Verification of Failure
Executing automated test suites using `pytest` confirmed that the application failed:
```bash
pytest
```
**Outcome:** `FAIL` — Service returned `500 Internal Server Error` due to `ZeroDivisionError`.

---

## 3. Identification & Reversal Strategy

### Step 3: Identifying the Faulty Commit
Using `git log`, the specific commit hash responsible for the breakage was identified:
```bash
git log --oneline -n 3
```
*Target Commit:* `wip: accidental bad commit that breaks health check`

### Step 4: Safe Rollback via `git revert`
To undo the breaking change without altering past history, `git revert` was executed:
```bash
git revert HEAD
```
Git automatically generated an inverse commit reversing the precise code changes from the faulty commit.

---

## 4. Verification & History Inspection

### Step 5: Post-Revert Test Verification
Re-running the automated test suite confirmed system stability:
```bash
pytest
```
**Outcome:** `PASS` — All tests returned green (`200 OK`).

### Step 6: Commit Log Inspection
Inspecting the history confirmed that both the bad commit and its reversal commit coexist transparently:
```bash
git log --oneline -n 5
```

---

## 5. Architectural Deep Dive: `git revert` vs `git reset`

| Criteria | `git revert` | `git reset` |
| :--- | :--- | :--- |
| **Mechanism** | Creates a **new commit** that reverses prior changes. | Rewinds the commit history back to a previous point. |
| **History Impact** | **Preserves history** (Non-destructive). | **Rewrites/Deletes history** (Destructive). |
| **Pushed / Shared Branches** | **Safe.** Does not cause history divergence for team members. | **Dangerous.** Causes out-of-sync errors for remote users. |
| **Best Used For** | Production bugs, public/shared branches, audited repos. | Local/unpushed commits, clean local workspace resets. |

### Conclusion: Why `git revert` is Preferred for Shared Repositories
When a bad commit has already been pushed to GitHub or shared with other engineers, `git reset` creates divergent local histories across team devices. This results in severe merge conflicts, force-push risks (`git push --force`), and lost tracking.

`git revert` avoids all synchronization errors by appending a forward-only commit. Every team member simply pulls the new commit, ensuring a clean, conflict-free, and fully auditable undo operation.