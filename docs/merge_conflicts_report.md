# Merge Conflict Resolution Documentation

## 1. Scenario Overview
A merge conflict occurred during the integration of `feature/dev-b-changes` into the `main` branch after `feature/dev-a-changes` was already merged. Both branches modified the exact same lines inside the `/health` endpoint in `main.py`.

## 2. Conflict Markers Encountered
When attempting the merge, Git inserted the following conflict markers into `main.py`:

```python
<<<<<<< HEAD
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "running"}
=======
@app.get("/health")
def health_check():
    return {"status": "up", "checks_passed": True}
>>>>>>> feature/dev-b-changes
```

* **`<<<<<<< HEAD` (Current Branch / Dev A):** Returned `{"status": "healthy", "service": "running"}`.
* **`=======`:** Separator between conflicting changes.
* **`>>>>>>> feature/dev-b-changes` (Incoming Branch / Dev B):** Returned `{"status": "up", "checks_passed": True}`.

## 3. Resolution Strategy
- To ensure that both developers' intended changes were preserved without discarding either feature  set, the conflict was resolved by merging the logic into a unified dictionary response:

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "running",
        "checks_passed": True
    }
```

## 4. Verification & Commit
- Verified the application logic and ensured clean syntax. 
- Finalized the resolution with a dedicated git commit:

```bash
git commit -m "fix: resolve merge conflict in health check, preserving both changes"
```
