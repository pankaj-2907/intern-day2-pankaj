# Git Recovery Lab - Comprehensive Documentation

---

## Exercise 1: Discarding Uncommitted Changes (`git restore`)

* **Initial State:** 
  `app.py` contains initial commit code (`Hello Recovery Lab`).
* **Command Executed:** 
  Added line `print("This is a bad change that I want to discard")` and saved. Then executed:
  ```bash
  git restore app.py
  ```
* **Result:** 
  Uncommitted changes were completely discarded from the working directory.
* **Final State:** 
  `app.py` reverted back to its last committed clean state (`Hello Recovery Lab`).
* **What You Learned:** 
  `git restore <file>` permanently discards uncommitted changes in the working directory without affecting git history.

---

## Exercise 2: Unstaging Changes (`git restore --staged`)

* **Initial State:** 
  `app.py` edited with `print("Adding new feature")` and staged using `git add app.py`. `git status` showed changes staged in green.
* **Command Executed:**
  ```bash
  git restore --staged app.py
  ```
* **Result:** 
  File was moved out of the Staging Area back to the Working Directory.
* **Final State:** 
  The code remained intact in `app.py`, but `git status` showed the changes in red (unstaged).
* **What You Learned:** 
  `git restore --staged <file>` safely undoes `git add` without deleting or modifying any code changes in the file.

---

## Exercise 3: Temporary Stashing (`git stash` & `git stash pop`)

* **Initial State:** 
  `app.py` had unfinished work in progress (`WIP: Work in progress code...`) that shouldn't be committed yet.
* **Command Executed:**
  ```bash
  git stash
  # Working directory became clean
  git stash pop
  ```
* **Result:** 
  `git stash` temporarily saved and stashed away local uncommitted modifications. `git stash pop` restored those stashed changes back into the working tree.
* **Final State:** 
  Unfinished work was hidden safely while working directory became clean, then successfully restored.
* **What You Learned:** 
  `git stash` acts as a temporary safe storage for uncommitted work when switching contexts, and `git stash pop` reapplies those changes when ready.

---

## Exercise 4: Commit Inspection (`git show`)

* **Initial State:** 
  Changes in `app.py` were added and committed with message `"feat: add feature and WIP code"`.
* **Command Executed:**
  ```bash
  git add app.py
  git commit -m "feat: add feature and WIP code"
  git show HEAD
  ```
* **Result:** 
  Terminal displayed a detailed diff view showing added (`+`) and removed (`-`) lines for the latest commit.
* **Final State:** 
  Commit was recorded in repository history, and its detailed changes were inspected.
* **What You Learned:** 
  `git show <commit_hash>` or `git show HEAD` inspects the line-by-line differences introduced by a specific commit.

---

## Exercise 5: Branching from History (`git switch -c`)

* **Initial State:** 
  Repository was on `main` branch with multiple recent commits.
* **Command Executed:** 
  Located initial commit hash using `git log --oneline` and ran:
  ```bash
  git switch -c feature/old-version-fix <initial-commit-hash>
  ```
* **Result:** 
  A new branch was created pointing to an older historical commit rather than the current HEAD.
* **Final State:** 
  Switched to `feature/old-version-fix` branch; `app.py` matched the state of the initial commit (`Hello Recovery Lab`).
* **What You Learned:** 
  Branches don't always need to start from the latest commit; `git switch -c <branch> <hash>` allows creating branches from any point in history.

---

## Exercise 6: Cherry-Picking Commit (`git cherry-pick`)

* **Initial State:** 
  Created a patch commit (`fix: apply critical patch on old branch`) on `feature/old-version-fix` branch.
* **Command Executed:** 
  Switched to `main` and executed:
  ```bash
  git switch main
  git cherry-pick <commit_hash>
  ```
* **Result:** 
  Copied the exact changes from that single commit onto `main` branch without merging the whole branch.
* **Final State:** 
  The specific fix commit was applied directly onto the `main` branch.
* **What You Learned:** 
  `git cherry-pick <commit_hash>` selectively applies changes from a specific commit from another branch into the current working branch.

---

## Exercise 7: Merge Conflict Resolution

* **Initial State:** 
  `app.py` on `main` branch had conflicting overlapping lines with the commit being cherry-picked from `feature/old-version-fix`.
* **Command Executed:** 
  Manually edited conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in `app.py`, then ran:
  ```bash
  git add app.py
  git cherry-pick --continue
  ```
* **Result:** 
  Conflict markers were cleared, desired code kept, and cherry-pick operation completed successfully.
* **Final State:** 
  `app.py` cleanly integrated both feature lines without syntax/conflict markers, and commit was finalized.
* **What You Learned:** 
  Conflicts occur when Git cannot automatically merge changes; resolving requires manual code selection, staging (`git add`), and continuing the operation.

---

## Exercise 8: Commit Tagging (`git tag`)

* **Initial State:** 
  A stable state was reached on the `main` branch.
* **Command Executed:**
  ```bash
  git tag -a v0.1.0 -m "Release version 0.1.0"
  git show v0.1.0
  ```
* **Result:** 
  An annotated tag named `v0.1.0` was created pointing to the current commit.
* **Final State:** 
  Tag `v0.1.0` permanently bookmarked the release commit in git history.
* **What You Learned:** 
  Annotated tags (`git tag -a`) serve as explicit release milestones/labels attached to specific commits in a repository.

---

## Exercise 9: Commit Graph Inspection (`git log --graph`)

* **Initial State:** 
  Repository contained multiple branches, tags, and commits.
* **Command Executed:**
  ```bash
  git log --oneline --graph --decorate --all
  ```
* **Result:** 
  A visual ASCII graph tree was rendered in the terminal showing branch splits, tags, and commit history.
* **Final State:** 
  Visual overview of all branches (`main`, `feature/old-version-fix`) and tags (`v0.1.0`) was displayed clearly.
* **What You Learned:** 
  `git log --oneline --graph --decorate --all` provides a complete visual representation of branch topography and history structure.

---

## Exercise 10: Recovering Lost Commits (`git reflog`)

* **Initial State:** 
  Created a new commit `"feat: temporary secret code"`, then accidentally lost it using hard reset (`git reset --hard HEAD~1`).
* **Command Executed:**
  ```bash
  git reflog
  # Identified the commit hash before reset
  git reset --hard <commit_hash>
  ```
* **Result:** 
  `git reflog` tracked the lost commit hash, allowing `git reset --hard` to jump back to that exact commit.
* **Final State:** 
  The "lost" commit and code changes in `app.py` were completely recovered.
* **What You Learned:** 
  `git reflog` records all local reference updates (HEAD movements). It acts as the ultimate safety net to recover lost commits, deleted branches, or bad resets.
