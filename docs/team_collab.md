# Part 5: Team Collaboration & Pull Request Simulation

This document records the simulation of a multi-developer environment using separate feature branches, pull requests, code reviews, and safe merging strategies.

## Workflow Overview

1. **Feature Branch Creation (Developer A):**
   - Created and switched to branch: `feature/word-frequency`
   - Added the word-frequency endpoint to `main.py`.
   - Pushed branch to remote:
     ```bash
     git switch -c feature/word-frequency
     git push origin feature/word-frequency
     ```

2. **Feature Branch Creation (Developer B):**
   - Switched back to `main`, pulled latest changes, and created: `feature/text-analysis-update`
   - Added text-analysis improvements to `main.py`.
   - Pushed branch to remote:
     ```bash
     git switch main && git pull origin main
     git switch -c feature/text-analysis-update
     git push origin feature/text-analysis-update
     ```

3. **Pull Request (PR) Lifecycle:**
   - Opened separate Pull Requests on GitHub for both branches targeting `main`.
   - Conducted code reviews using the standard PR review checklist.
   - Added meaningful review comments regarding code logic, input validation, and test coverage.

4. **Review Checklist Verification:**
   -  Code meets functional requirements.
   -  Tests (`pytest`) pass successfully.
   -  Commit messages follow clear conventions (`feat: ...`).
   -  Unrelated changes excluded.

5. **Merging and Synchronization:**
   - Approved and merged both PRs into `main` via GitHub UI.
   - Pulled the latest synchronized `main` branch locally and verified with `pytest`:
     ```bash
     git switch main
     git pull origin main
     pytest
     ```