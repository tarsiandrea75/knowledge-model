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
BUDGET_SAFETY_FACTOR="${BUDGET_SAFETY_FACTOR:-1.25}"
BUDGET_GRACE_TOKENS="${BUDGET_GRACE_TOKENS:-10000}"
BUDGET_GRACE_RATIO="${BUDGET_GRACE_RATIO:-0.02}"
FORCE="${FORCE:-false}"
PER_CYCLE_TIMEOUT_SECONDS="${RKM_PER_CYCLE_TIMEOUT_SECONDS:-3600}"
BUDGET_ESTIMATE_OUTPUT=""

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

parse_bool() {
  local value
  value="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    true|1|yes|y|on) return 0 ;;
    false|0|no|n|off|"") return 1 ;;
    *) fail "Invalid FORCE value: $1. Expected true, false, 1, 0, yes, no, y, n, on, or off." ;;
  esac
}

current_time() {
  date '+%Y-%m-%d %H:%M:%S %Z'
}

current_epoch() {
  date '+%s'
}

current_utc_iso() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
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

require_gnu_timeout() {
  local timeout_version

  require_command timeout
  timeout_version="$(timeout --version 2>/dev/null || true)"
  [[ "$timeout_version" == *"GNU coreutils"* ]] \
    || fail "GNU timeout is required for per-cycle timeout enforcement. Install GNU coreutils timeout or run on an environment where it is available."
}

validate_non_negative_number() {
  local label="$1"
  local value="$2"

  awk -v value="$value" -v label="$label" '
    BEGIN {
      if (value !~ /^[0-9]+([.][0-9]+)?$/) {
        printf("ERROR: %s must be a non-negative number: %s\n", label, value) > "/dev/stderr"
        exit 1
      }
    }
  ' || exit 1
}

validate_positive_integer() {
  local label="$1"
  local value="$2"

  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -lt 1 ]]; then
    fail "$label must be a positive integer: $value"
  fi
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

run_with_heartbeat() {
  local label="$1"
  local log_path="$2"
  local timeout_seconds="$3"
  shift 3

  local start_epoch
  local next_heartbeat_elapsed
  local current_elapsed
  local child_pid
  local child_status

  start_epoch="$(current_epoch)"
  next_heartbeat_elapsed=30
  if [[ -n "$timeout_seconds" ]]; then
    timeout --kill-after=30s "${timeout_seconds}s" "$@" >"$log_path" 2>&1 &
  else
    "$@" >"$log_path" 2>&1 &
  fi
  child_pid="$!"

  while is_running_job "$child_pid"; do
    sleep 1
    current_elapsed="$(($(current_epoch) - start_epoch))"
    if [[ "$current_elapsed" -ge "$next_heartbeat_elapsed" ]] && is_running_job "$child_pid"; then
      progress "$label still running. Elapsed: $(format_elapsed "$current_elapsed"). Log: $log_path"
      next_heartbeat_elapsed=$((next_heartbeat_elapsed + 30))
    fi
  done

  if wait "$child_pid"; then
    child_status=0
  else
    child_status="$?"
  fi

  return "$child_status"
}

is_running_job() {
  local target_pid="$1"
  local running_pid

  while read -r running_pid; do
    if [[ "$running_pid" == "$target_pid" ]]; then
      return 0
    fi
  done < <(jobs -pr)

  return 1
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

run_budget_estimate() {
  local target="$1"
  local estimate_output
  local estimate_result

  BUDGET_ESTIMATE_OUTPUT=""

  if [[ -z "${TOKEN_BUDGET:-}" ]]; then
    return 0
  fi

  if [[ ! -f "$LEDGER_SCRIPT" ]]; then
    warn "Ledger script not found: $LEDGER_SCRIPT; token budget guard skipped."
    return 0
  fi

  if estimate_output="$(
    python3 "$LEDGER_SCRIPT" estimate \
      --target "$target" \
      --budget "$TOKEN_BUDGET" \
      --since "$AUTOCYCLE_STARTED_AT_UTC" \
      --safety-factor "$BUDGET_SAFETY_FACTOR" 2>&1
  )"; then
    estimate_result=0
  else
    estimate_result="$?"
  fi

  if [[ -n "$estimate_output" ]]; then
    printf '%s\n' "$estimate_output"
  fi
  BUDGET_ESTIMATE_OUTPUT="$estimate_output"

  if [[ "$estimate_result" -eq 2 ]] && [[ "$estimate_output" == Estimation\ unavailable:* ]]; then
    warn "Token budget estimate history is unavailable; continuing without budget guard."
    return 0
  fi

  return "$estimate_result"
}

budget_estimate_field() {
  local field="$1"

  awk -F': ' -v field="$field" '$1 == field { print $2; exit }' <<<"$BUDGET_ESTIMATE_OUTPUT"
}

budget_near_miss_within_grace() {
  local estimated_tokens
  local remaining_budget

  estimated_tokens="$(budget_estimate_field "estimatedTokens")"
  remaining_budget="$(budget_estimate_field "remainingBudget")"

  if [[ -z "$estimated_tokens" || -z "$remaining_budget" ]]; then
    return 1
  fi

  awk \
    -v estimated_tokens="$estimated_tokens" \
    -v remaining_budget="$remaining_budget" \
    -v grace_tokens="$BUDGET_GRACE_TOKENS" \
    -v grace_ratio="$BUDGET_GRACE_RATIO" '
      BEGIN {
        shortfall = estimated_tokens - remaining_budget
        ratio_grace_tokens = estimated_tokens * grace_ratio
        grace_allowed = grace_tokens > ratio_grace_tokens ? grace_tokens : ratio_grace_tokens
        if (shortfall <= grace_allowed) {
          printf("[rkm-autocycle] WARNING: token budget guard near miss; shortfall %.2f within grace %.2f; continuing.\n", shortfall, grace_allowed) > "/dev/stderr"
          exit 0
        }
        exit 1
      }
    '
}

handle_budget_result() {
  local budget_result="$1"
  local stop_message="$2"

  if [[ "$budget_result" -eq 3 ]]; then
    if [[ "$force_enabled" == "true" ]]; then
      warn "token budget guard would stop here, but FORCE=true; continuing."
      return 0
    fi
    if budget_near_miss_within_grace; then
      return 0
    fi
    printf '%s\n' "$stop_message" >&2
    return 1
  fi

  return 0
}

validate_positive_integer "RKM_PER_CYCLE_TIMEOUT_SECONDS" "$PER_CYCLE_TIMEOUT_SECONDS"

if [[ "$TARGET_ACCEPTED_FILES" == "--validate-timeout-only" ]]; then
  progress "Per-cycle timeout accepted: ${PER_CYCLE_TIMEOUT_SECONDS} seconds."
  exit 0
fi

if ! [[ "$TARGET_ACCEPTED_FILES" =~ ^[0-9]+$ ]] || [[ "$TARGET_ACCEPTED_FILES" -lt 1 ]]; then
  fail "Accepted file target must be a positive integer."
fi

require_command git
require_command bash
require_command make
require_gnu_timeout
require_command tail
require_command wc
require_command awk

ensure_clean_worktree
validate_non_negative_number "BUDGET_GRACE_TOKENS" "$BUDGET_GRACE_TOKENS"
validate_non_negative_number "BUDGET_GRACE_RATIO" "$BUDGET_GRACE_RATIO"

force_enabled=false
if parse_bool "$FORCE"; then
  force_enabled=true
  warn "FORCE mode enabled: token budget guard warnings will not stop autocycle."
fi

accepted_files=0
autocycle_start_epoch="$(current_epoch)"
AUTOCYCLE_STARTED_AT_UTC="$(current_utc_iso)"
progress "Autocycle started at $(current_time)."

if [[ -n "${TOKEN_BUDGET:-}" ]]; then
  initial_budget_result=0
  if run_budget_estimate "$TARGET_ACCEPTED_FILES"; then
    initial_budget_result=0
  else
    initial_budget_result="$?"
  fi

  if [[ "$initial_budget_result" -eq 3 ]]; then
    if ! handle_budget_result "$initial_budget_result" "ERROR: Token budget guard stopped before work: budget is insufficient for $TARGET_ACCEPTED_FILES accepted file(s)."; then
      exit 1
    fi
    initial_budget_result=0
  fi

  if [[ "$initial_budget_result" -ne 0 ]]; then
    fail "Token budget estimate failed before work."
  fi
fi

while [[ "$accepted_files" -lt "$TARGET_ACCEPTED_FILES" ]]; do
  iteration=$((accepted_files + 1))
  iteration_start_epoch="$(current_epoch)"
  cycle_result=0
  recovery_result=0
  reviewer_verdict=""
  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES started at $(current_time)."

  if run_with_heartbeat "cycle attempt" "$CYCLE_OUTPUT" "$PER_CYCLE_TIMEOUT_SECONDS" bash scripts/rkm-cycle.sh 1; then
    cycle_result=0
  else
    cycle_result=$?
  fi

  append_ledger_log "$CYCLE_OUTPUT" "autocycle-cycle"

  if [[ "$cycle_result" -eq 124 || "$cycle_result" -eq 137 ]]; then
    printf 'ERROR: cycle attempt timed out after %s seconds during iteration %s of %s.\n' "$PER_CYCLE_TIMEOUT_SECONDS" "$iteration" "$TARGET_ACCEPTED_FILES" >&2
    printf 'Log: %s\n' "$CYCLE_OUTPUT" >&2
    printf 'Inspect git status --short before continuing.\n' >&2
    git status --short
    exit 124
  fi

  if [[ "$cycle_result" -eq 0 ]]; then
    accepted_files=$((accepted_files + 1))
    iteration_end_epoch="$(current_epoch)"
    progress "Iteration $iteration of $TARGET_ACCEPTED_FILES accepted by rkm-cycle.sh. Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
    git log --oneline -n 1
    remaining_target=$((TARGET_ACCEPTED_FILES - accepted_files))
    if [[ -n "${TOKEN_BUDGET:-}" ]] && [[ "$remaining_target" -gt 0 ]]; then
      budget_result=0
      if run_budget_estimate "$remaining_target"; then
        budget_result=0
      else
        budget_result="$?"
      fi
      if [[ "$budget_result" -eq 3 ]]; then
        if ! handle_budget_result "$budget_result" "ERROR: Token budget guard stopped after iteration $iteration: remaining budget is insufficient for $remaining_target more accepted file(s)."; then
          print_ledger_report
          git status --short
          exit 1
        fi
        budget_result=0
      fi
      if [[ "$budget_result" -ne 0 ]]; then
        fail "Token budget estimate failed after iteration $iteration."
      fi
    fi
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
  if run_with_heartbeat "recovery attempt" "$RECOVER_OUTPUT" "" bash scripts/rkm-recover-revise.sh; then
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
    remaining_target=$((TARGET_ACCEPTED_FILES - accepted_files))
    if [[ -n "${TOKEN_BUDGET:-}" ]] && [[ "$remaining_target" -gt 0 ]]; then
      budget_result=0
      if run_budget_estimate "$remaining_target"; then
        budget_result=0
      else
        budget_result="$?"
      fi
      if [[ "$budget_result" -eq 3 ]]; then
        if ! handle_budget_result "$budget_result" "ERROR: Token budget guard stopped after iteration $iteration: remaining budget is insufficient for $remaining_target more accepted file(s)."; then
          print_ledger_report
          git status --short
          exit 1
        fi
        budget_result=0
      fi
      if [[ "$budget_result" -ne 0 ]]; then
        fail "Token budget estimate failed after iteration $iteration."
      fi
    fi
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
