# Scenario 6: Handling a Remote-Behind Local Branch

When another developer pushes changes to the remote repository (GitHub), your local branch becomes **behind**. 

## Step-by-Step Workflow

1. **Simulate Remote Change:**
   Make a small change directly on GitHub (e.g., updating `main.py` or `README.md`) and commit it. Your local repository is now behind.

2. **Fetch Remote Metadata (Without Modifying Local Files):**
   ```bash
   git fetch origin
   ```
   This downloads the latest history and changes from the remote repository to your local machine safely.

3. **Inspect the New Remote History:**
   ```bash
   git log origin/main --oneline -n 3
   ```
   View the new commits that exist on the remote branch before merging them.

4. **Integrate Changes into Local:**
   ```bash
   git pull origin main
   ```
   This downloads and merges the remote changes into your active local workspace.

## Key Concept: Fetch vs. Integrate

* **`git fetch`:** Downloads updates and history from remote without altering your working files. Safe to run anytime.
* **`git pull` (or Merge):** Combines/integrates those fetched changes into your current working code directory.

