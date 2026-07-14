# Unattended Autopilot

## Purpose

Run bounded automation while preserving clean checkpoints, validation discipline, and recoverable logs.

## When to Use

Use this guide before any unattended or away-from-keyboard autopilot run.

## Required Readings

- `AGENTS.md`
- `docs/maintenance/automation-guardrails.md`

## Required Checks

- Confirm `git status --short` is clean before starting.
- Prefer repeated `make autopilot N=1` rounds.
- Write logs to `/tmp/rkm-runs`.
- Require validation, safe push, and cockpit summary after each round.

## Safe Command Loop

```bash
mkdir -p /tmp/rkm-runs
set -o pipefail
for i in 1 2 3 4 5 6 7 8 9 10
do
  LOG="/tmp/rkm-runs/autopilot-away-round-${i}.log"
  echo "===== AUTOPILOT ROUND $i =====" | tee -a "$LOG"
  date | tee -a "$LOG"
  make autopilot N=1 2>&1 | tee -a "$LOG" || break
  make safe-push 2>&1 | tee -a "$LOG" || break
  make validate 2>&1 | tee -a "$LOG" || break
  make cockpit-summary N=5 2>&1 | tee -a "$LOG" || break
  echo "===== END ROUND $i =====" | tee -a "$LOG"
done
```

## Budget-Stop Interpretation

A budget-stop after accepted commits is not a failure when the repository is clean and accepted commits were pushed. A budget-stop with a dirty worktree requires manual inspection before more automation.

## Common Failure Modes

- Running a large `N` unattended and spending budget on repeated recovery attempts.
- Writing logs inside the repository.
- Continuing after a dirty worktree or recovery requirement.
- Treating `FORCE=true` as permission to bypass validation or recovery.

## Done Criteria

- Each successful round validated, pushed through `make safe-push`, and emitted `make cockpit-summary N=5`.
- Logs are under `/tmp/rkm-runs`.
- The final state is clean, or automation stopped at a clearly reported recovery point.
