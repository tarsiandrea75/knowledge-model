#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TARGET_ACCEPTED_FILES="${1:-3}"
CYCLE_OUTPUT="/tmp/rkm-cycle-output.txt"
RECOVER_OUTPUT="/tmp/rkm-recover-revise-output.txt"
REVIEW_OUTPUT="/tmp/rkm-recover-revise-review.txt"
TAIL_LINES="${TAIL_LINES:-80}"
LEDGER_SCRIPT="scripts/rkm-run-ledger.py"
REVIEW_VERDICT_SCRIPT="scripts/rkm-review-verdict.py"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

progress() {
  printf '[rkm-autocycle] %s\n' "$1" >&2
}

warn() {
  printf '[rkm-autocycle] WARNING: %s\n' "$1" >&2
}

current_time() {
  date '+%Y-%m-%d %H:%M:%S %Z'
}

current_epoch() {
  date '+%s'
}

format_elapsed() {
  local elapsed_seconds="$1"
  local hours
  local minutes
  local seconds

  hours=$((elapsed_seconds / 3600))
  minutes=$(((elapsed_seconds % 3600) / 60))
  seconds=$((elapsed_seconds % 60))

  printf '%02d:%02d:%02d' "$hours" "$minutes" "$seconds"
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

ensure_clean_worktree() {
  if [[ -n "$(git status --porcelain)" ]]; then
    git status --short
    fail "Working tree must be clean before starting the RKM autocycle."
  fi
}

append_ledger_log() {
  local log_path="$1"
  local label="$2"

  if [[ ! -f "$LEDGER_SCRIPT" ]]; then
    warn "Ledger script not found: $LEDGER_SCRIPT"
    return 0
  fi

  if [[ ! -f "$log_path" ]]; then
    return 0
  fi

  if ! python3 "$LEDGER_SCRIPT" append --log "$log_path" --label "$label"; then
    warn "Ledger append failed for $log_path with label $label."
  fi
}

print_ledger_report() {
  if [[ ! -f "$LEDGER_SCRIPT" ]]; then
    warn "Ledger script not found: $LEDGER_SCRIPT"
    return 0
  fi

  if ! python3 "$LEDGER_SCRIPT" report; then
    warn "Ledger report failed."
  fi
}

if ! [[ "$TARGET_ACCEPTED_FILES" =~ ^[0-9]+$ ]] || [[ "$TARGET_ACCEPTED_FILES" -lt 1 ]]; then
  fail "Accepted file target must be a positive integer."
fi

require_command git
require_command bash
require_command make
require_command tail
require_command wc

ensure_clean_worktree

accepted_files=0
autocycle_start_epoch="$(current_epoch)"
progress "Autocycle started at $(current_time)."

while [[ "$accepted_files" -lt "$TARGET_ACCEPTED_FILES" ]]; do
  iteration=$((accepted_files + 1))
  iteration_start_epoch="$(current_epoch)"
  cycle_result=0
  recovery_result=0
  reviewer_verdict=""
  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES started at $(current_time)."

  if bash scripts/rkm-cycle.sh 1 >"$CYCLE_OUTPUT" 2>&1; then
    cycle_result=0
  else
    cycle_result=$?
  fi

  append_ledger_log "$CYCLE_OUTPUT" "autocycle-cycle"

  if [[ "$cycle_result" -eq 0 ]]; then
    accepted_files=$((accepted_files + 1))
    iteration_end_epoch="$(current_epoch)"
    progress "Iteration $iteration of $TARGET_ACCEPTED_FILES accepted by rkm-cycle.sh. Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
    git log --oneline -n 1
    continue
  fi

  if [[ -f "$REVIEW_VERDICT_SCRIPT" ]]; then
    if reviewer_verdict="$(python3 "$REVIEW_VERDICT_SCRIPT" "$CYCLE_OUTPUT" 2>/dev/null)"; then
      :
    else
      reviewer_verdict=""
    fi
  fi

  if [[ "$reviewer_verdict" == "STOP" ]]; then
    printf 'Reviewer returned STOP; recovery will not be attempted.\n' >&2
    print_ledger_report
    git status --short
    exit 1
  fi

  if [[ "$reviewer_verdict" != "REVISE" ]]; then
    printf 'ERROR: Could not parse explicit reviewer verdict from %s; recovery will not be attempted.\n' "$CYCLE_OUTPUT" >&2
    printf '\nrkm-cycle.sh output tail (%s lines):\n' "$TAIL_LINES"
    tail -n "$TAIL_LINES" "$CYCLE_OUTPUT"
    git status --short
    exit 1
  fi

  printf '\nrkm-cycle.sh output tail (%s lines):\n' "$TAIL_LINES"
  tail -n "$TAIL_LINES" "$CYCLE_OUTPUT"

  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES entering single-file REVISE recovery at $(current_time)."
  if bash scripts/rkm-recover-revise.sh; then
    recovery_result=0
  else
    recovery_result=$?
  fi

  append_ledger_log "$RECOVER_OUTPUT" "autocycle-recovery"
  append_ledger_log "$REVIEW_OUTPUT" "autocycle-recovery-review"

  if [[ "$recovery_result" -eq 0 ]]; then
    accepted_files=$((accepted_files + 1))
    iteration_end_epoch="$(current_epoch)"
    progress "Iteration $iteration of $TARGET_ACCEPTED_FILES accepted after recovery. Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
    git log --oneline -n 1
    continue
  fi

  printf 'ERROR: REVISE recovery failed during iteration %s of %s.\n' "$iteration" "$TARGET_ACCEPTED_FILES" >&2
  git status --short
  exit 1
done

autocycle_end_epoch="$(current_epoch)"
progress "Autocycle ended at $(current_time). Elapsed: $(format_elapsed "$((autocycle_end_epoch - autocycle_start_epoch))")."
progress "Autocycle completed: $accepted_files accepted file(s) committed."
print_ledger_report
git status --short
