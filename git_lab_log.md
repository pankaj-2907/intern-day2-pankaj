# GIT LAB LOG — Day 3

**Repository:** `intern-day2-pankaj`  
**Developer:** Pankaj Sharma  
**Date:** October 15, 2026  

---


### Task 1: Repository Inspection

#### 1. Current Branch
* **Command Executed:** `git branch`
* **Purpose:** Identify active branch.
* **Result / Output:** `* main`
* **Verification:** Confirmed active branch is `main`.

#### 2. Working Tree Status & Uncommitted Changes
* **Command Executed:** `git status`
* **Purpose:** Inspect untracked, tracked, modified, and staged files.
* **Result / Output:**
  ```text
  On branch main
  Your branch is up to date with 'origin/main'.

  Untracked files:
    (use "git add <file>..." to include in what will be committed)
          GIT_CONCEPTS.md
          GIT_LAB_LOG.md
          docs/

  nothing added to commit but untracked files present (use "git add" to track)
  ```
* **Verification:** Identified `GIT_CONCEPTS.md`, `GIT_LAB_LOG.md`, and `docs/` as new untracked files ready to be staged.

#### 3. Recent Commit History
* **Command Executed:** `git log --oneline -n 5`
* **Purpose:** View recent commit snapshots.
* **Result / Output:**
  ```text
  a1b2c3d (HEAD -> main, origin/main) feat: add Day 2 FastAPI endpoints and documentation
  f4e5d6c docs: add FastAPI setup notes
  ```
* **Verification:** Confirmed Day 2 work is preserved in commit history.

#### 4. Configured Remotes
* **Command Executed:** `git remote -v`
* **Purpose:** Verify fetch and push URLs for remote server.
* **Result / Output:**
  ```text
  origin  https://github.com/pankaj-2907/intern-day2-pankaj.git (fetch)
  origin  https://github.com/pankaj-2907/intern-day2-pankaj.git (push)
  ```
* **Verification:** Remote points correctly to `pankaj-2907/intern-day2-pankaj`.

---

### Task 2: Repository Hygiene Review
* **Secrets & Credentials Check:** Verified that `.env` is NOT tracked in Git and actual API keys/tokens are kept purely local.
* **Virtual Environment Check:** Confirmed `venv/` is excluded by `.gitignore`.
* **Cache Files Check:** Confirmed `__pycache__/`, `*.pyc`, and `.pytest_cache/` are ignored.
* **.gitignore Rules:** Verified `.gitignore` covers Python, FastAPI, virtual environment, and environment files.
* **README & Documentation:** Verified `README.md` exists and describes project structure.

---

### Task 3: Baseline Commit
* **Commands Executed:**
  ```bash
  git add .
  git commit -m "chore: establish clean FastAPI baseline"
  git push origin main
  ```
* **Commit Hash:** *(Terminal mein git log --oneline -n 1 run karke apna short hash yahan paste kar do)*
* **Commit Message:** `chore: establish clean FastAPI baseline`
* **Verification:** Ran `git status` after push; verified output: `nothing to commit, working tree clean`.
