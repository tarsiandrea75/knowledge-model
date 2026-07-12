#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TARGET_ACCEPTED_FILES="${1:-3}"
CYCLE_OUTPUT="/tmp/rkm-cycle-output.txt"
TAIL_LINES="${TAIL_LINES:-80}"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

progress() {
  printf '[rkm-autocycle] %s\n' "$1" >&2
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
  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES started at $(current_time)."

  if bash scripts/rkm-cycle.sh 1 >"$CYCLE_OUTPUT" 2>&1; then
    accepted_files=$((accepted_files + 1))
    iteration_end_epoch="$(current_epoch)"
    progress "Iteration $iteration of $TARGET_ACCEPTED_FILES accepted by rkm-cycle.sh. Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
    continue
  fi

  printf '\nrkm-cycle.sh output tail (%s lines):\n' "$TAIL_LINES"
  tail -n "$TAIL_LINES" "$CYCLE_OUTPUT"

  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES entering single-file REVISE recovery at $(current_time)."
  if bash scripts/rkm-recover-revise.sh; then
    accepted_files=$((accepted_files + 1))
    iteration_end_epoch="$(current_epoch)"
    progress "Iteration $iteration of $TARGET_ACCEPTED_FILES accepted after recovery. Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
    continue
  fi

  printf 'ERROR: REVISE recovery failed during iteration %s of %s.\n' "$iteration" "$TARGET_ACCEPTED_FILES" >&2
  git status --short
  exit 1
done

autocycle_end_epoch="$(current_epoch)"
progress "Autocycle ended at $(current_time). Elapsed: $(format_elapsed "$((autocycle_end_epoch - autocycle_start_epoch))")."
progress "Autocycle completed: $accepted_files accepted file(s) committed."
git status --short
