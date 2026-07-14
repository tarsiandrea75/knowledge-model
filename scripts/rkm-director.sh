#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

EXPECTED_BRANCH="experiment/codex-director"
EXPECTED_UPSTREAM="origin/experiment/codex-director"
PROMPT_FILE="docs/maintenance/rkm-director-prompt.md"
RUN_ROOT="/tmp/rkm-runs"

HARD_TIMEOUT_SECONDS="${RKM_DIRECTOR_TIMEOUT_SECONDS:-7200}"
HEARTBEAT_SECONDS="${RKM_DIRECTOR_HEARTBEAT_SECONDS:-30}"
TAIL_LINES="${TAIL_LINES:-100}"

SELF_TEST=false
WATCHDOG_PID=""
LOCK_DIR=""
LOG_FILE=""
FINAL_REPORT=""
STATUS_FILE=""
MAIN_BEFORE=""
ORIGIN_MAIN_BEFORE=""
INTERRUPT_REQUESTED=false

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

progress() {
  printf '[rkm-director] %s\n' "$1" >&2
}

warn() {
  printf '[rkm-director] WARNING: %s\n' "$1" >&2
}

usage() {
  cat >&2 <<'USAGE_EOF'
Usage:
  bash scripts/rkm-director.sh
  bash scripts/rkm-director.sh --self-test
  bash scripts/rkm-director.sh --help

Environment variables:
  RKM_DIRECTOR_TIMEOUT_SECONDS     Hard watchdog timeout. Default: 7200
  RKM_DIRECTOR_HEARTBEAT_SECONDS   Heartbeat interval. Default: 30
  TAIL_LINES                       Lines shown after a failure. Default: 100
USAGE_EOF
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 \
    || fail "Required command not found: $command_name"
}

is_positive_integer() {
  local value="${1:-}"
  [[ "$value" =~ ^[0-9]+$ ]] && [[ "$value" -ge 1 ]]
}

validate_positive_integer() {
  local label="$1"
  local value="$2"

  is_positive_integer "$value" \
    || fail "$label must be a positive integer: $value"
}

require_gnu_timeout() {
  local timeout_version

  require_command timeout
  timeout_version="$(timeout --version 2>/dev/null || true)"

  [[ "$timeout_version" == *"GNU coreutils"* ]] \
    || fail "GNU coreutils timeout is required."
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

effective_director_exit() {
  local child_exit="$1"

  if [[ "$INTERRUPT_REQUESTED" == true ]]; then
    printf '130'
  else
    printf '%s' "$child_exit"
  fi
}

final_report_is_present() {
  local report_path="$1"
  [[ -s "$report_path" ]]
}

print_artifact_paths() {
  printf '\nDirector runtime artifacts:\n'
  printf '  Log:          %s\n' "${LOG_FILE:-not-created}"
  printf '  Final report: %s\n' "${FINAL_REPORT:-not-created}"
  printf '  Status:       %s\n' "${STATUS_FILE:-not-created}"
}

print_log_tail() {
  if [[ -n "$LOG_FILE" && -f "$LOG_FILE" ]]; then
    printf '\nLast %s log lines:\n' "$TAIL_LINES" >&2
    tail -n "$TAIL_LINES" "$LOG_FILE" >&2
  fi
}

cleanup() {
  if [[ -n "${WATCHDOG_PID:-}" ]] && kill -0 "$WATCHDOG_PID" 2>/dev/null; then
    kill -TERM "$WATCHDOG_PID" 2>/dev/null || true
    wait "$WATCHDOG_PID" 2>/dev/null || true
  fi

  if [[ -n "${LOCK_DIR:-}" && -d "$LOCK_DIR" ]]; then
    rmdir "$LOCK_DIR" 2>/dev/null || true
  fi
}

handle_signal() {
  local signal_name="$1"

  INTERRUPT_REQUESTED=true
  warn "Received $signal_name; requesting an orderly Director interruption."

  if [[ -n "${WATCHDOG_PID:-}" ]] && kill -0 "$WATCHDOG_PID" 2>/dev/null; then
    kill -INT "$WATCHDOG_PID" 2>/dev/null || true
  fi
}

require_prompt_contract() {
  local marker
  local markers=(
    "# RKM Codex Director Operating Contract"
    "Act as the autonomous RKM Director."
    'experiment/codex-director'
    '`rkm_worker`'
    '`rkm_reviewer`'
    '`make safe-push`'
    "Direct \`git push\` is prohibited"
    "## Protected Change Categories"
    "## Stop Conditions"
    "## Finalization"
  )

  [[ -f "$PROMPT_FILE" ]] \
    || fail "Director prompt does not exist: $PROMPT_FILE"

  for marker in "${markers[@]}"; do
    grep -Fq "$marker" "$PROMPT_FILE" \
      || fail "Director prompt is missing required contract marker: $marker"
  done
}

ensure_clean_worktree() {
  if [[ -n "$(git status --porcelain)" ]]; then
    git status --short
    fail "Working tree must be clean before starting the RKM Director."
  fi
}

ensure_expected_branch() {
  local current_branch

  current_branch="$(git branch --show-current)"

  [[ "$current_branch" == "$EXPECTED_BRANCH" ]] \
    || fail "Expected branch $EXPECTED_BRANCH, found $current_branch."
}

ensure_expected_upstream() {
  local upstream
  local ahead
  local behind

  upstream="$(
    git rev-parse \
      --abbrev-ref \
      --symbolic-full-name \
      '@{upstream}' 2>/dev/null
  )" || fail "Current branch has no upstream."

  [[ "$upstream" == "$EXPECTED_UPSTREAM" ]] \
    || fail "Expected upstream $EXPECTED_UPSTREAM, found $upstream."

  ahead="$(git rev-list --count '@{upstream}'..HEAD)"
  behind="$(git rev-list --count HEAD..'@{upstream}')"

  [[ "$ahead" == "0" && "$behind" == "0" ]] \
    || fail "Branch must be aligned with upstream before launch. Ahead: $ahead. Behind: $behind."
}

ensure_origin() {
  local origin_url

  origin_url="$(git remote get-url origin 2>/dev/null)" \
    || fail "Git remote origin is not configured."

  [[ -n "$origin_url" ]] \
    || fail "Git remote origin has an empty URL."
}

capture_protected_refs() {
  MAIN_BEFORE="$(git rev-parse main)"
  ORIGIN_MAIN_BEFORE="$(git rev-parse origin/main)"
}

verify_protected_refs() {
  local main_after
  local origin_main_after

  main_after="$(git rev-parse main)"
  origin_main_after="$(git rev-parse origin/main)"

  [[ "$main_after" == "$MAIN_BEFORE" ]] \
    || fail "Local main changed during the Director session."

  [[ "$origin_main_after" == "$ORIGIN_MAIN_BEFORE" ]] \
    || fail "origin/main changed in the local repository during the Director session."
}

create_runtime_paths() {
  local run_id

  mkdir -p "$RUN_ROOT"

  LOCK_DIR="$RUN_ROOT/director.lock"

  if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    fail "Another Director session may already be active: $LOCK_DIR"
  fi

  run_id="$(date -u '+%Y%m%dT%H%M%SZ')-$$"
  LOG_FILE="$RUN_ROOT/director-$run_id.log"
  FINAL_REPORT="$RUN_ROOT/director-$run_id-final.txt"
  STATUS_FILE="$RUN_ROOT/director-$run_id-status.txt"

  : > "$LOG_FILE"
  : > "$FINAL_REPORT"

  {
    printf 'state=STARTING\n'
    printf 'startUtc=%s\n' "$(current_utc_iso)"
    printf 'branch=%s\n' "$EXPECTED_BRANCH"
    printf 'commit=%s\n' "$(git rev-parse HEAD)"
    printf 'hardTimeoutSeconds=%s\n' "$HARD_TIMEOUT_SECONDS"
    printf 'logFile=%s\n' "$LOG_FILE"
    printf 'finalReport=%s\n' "$FINAL_REPORT"
  } > "$STATUS_FILE"
}

write_final_status() {
  local state="$1"
  local exit_code="$2"
  local elapsed_seconds="$3"

  {
    printf 'state=%s\n' "$state"
    printf 'endUtc=%s\n' "$(current_utc_iso)"
    printf 'exitCode=%s\n' "$exit_code"
    printf 'elapsedSeconds=%s\n' "$elapsed_seconds"
    printf 'elapsed=%s\n' "$(format_elapsed "$elapsed_seconds")"
    printf 'branch=%s\n' "$(git branch --show-current)"
    printf 'commit=%s\n' "$(git rev-parse HEAD)"
    printf 'logFile=%s\n' "$LOG_FILE"
    printf 'finalReport=%s\n' "$FINAL_REPORT"
  } > "$STATUS_FILE"
}

run_self_test() {
  local invalid_value

  [[ "$(format_elapsed 0)" == "00:00:00" ]] \
    || fail "Self-test failed: zero elapsed-time formatting."

  [[ "$(format_elapsed 3661)" == "01:01:01" ]] \
    || fail "Self-test failed: elapsed-time formatting."

  is_positive_integer 1 \
    || fail "Self-test failed: positive integer 1 was rejected."

  is_positive_integer 7200 \
    || fail "Self-test failed: positive integer 7200 was rejected."

  for invalid_value in 0 -1 invalid 1.5 ""; do
    if is_positive_integer "$invalid_value"; then
      fail "Self-test failed: invalid positive integer was accepted: $invalid_value"
    fi
  done

  [[ "$RUN_ROOT" == "/tmp/rkm-runs" ]] \
    || fail "Self-test failed: runtime output must remain under /tmp/rkm-runs."

  [[ "$EXPECTED_BRANCH" == "experiment/codex-director" ]] \
    || fail "Self-test failed: experimental branch guard changed."

  [[ "$EXPECTED_UPSTREAM" == "origin/experiment/codex-director" ]] \
    || fail "Self-test failed: experimental upstream guard changed."

  INTERRUPT_REQUESTED=false
  [[ "$(effective_director_exit 0)" == "0" ]] \
    || fail "Self-test failed: normal child exit was changed."

  INTERRUPT_REQUESTED=true
  [[ "$(effective_director_exit 0)" == "130" ]] \
    || fail "Self-test failed: interruption did not normalize to exit 130."

  INTERRUPT_REQUESTED=false

  if final_report_is_present /dev/null; then
    fail "Self-test failed: empty final report was accepted."
  fi

  require_prompt_contract

  final_report_is_present "$PROMPT_FILE" \
    || fail "Self-test failed: non-empty report detection failed."

  printf 'RKM Director launcher self-test passed.\n'
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --self-test)
      SELF_TEST=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage
      fail "Unknown argument: $1"
      ;;
  esac
done

validate_positive_integer \
  "RKM_DIRECTOR_TIMEOUT_SECONDS" \
  "$HARD_TIMEOUT_SECONDS"

validate_positive_integer \
  "RKM_DIRECTOR_HEARTBEAT_SECONDS" \
  "$HEARTBEAT_SECONDS"

validate_positive_integer \
  "TAIL_LINES" \
  "$TAIL_LINES"

if [[ "$SELF_TEST" == true ]]; then
  run_self_test
  exit 0
fi

require_command codex
require_command date
require_command git
require_command grep
require_command mkdir
require_command tail
require_gnu_timeout
require_prompt_contract

trap cleanup EXIT
trap 'handle_signal INT' INT
trap 'handle_signal TERM' TERM

progress "Fetching current origin references."
git fetch --prune origin

ensure_expected_branch
ensure_expected_upstream
ensure_origin
ensure_clean_worktree
capture_protected_refs
create_runtime_paths

start_epoch="$(current_epoch)"
next_heartbeat_elapsed="$HEARTBEAT_SECONDS"

progress "Starting autonomous Director."
progress "Hard timeout: $(format_elapsed "$HARD_TIMEOUT_SECONDS")."
progress "Log: $LOG_FILE"
progress "Final report: $FINAL_REPORT"

{
  printf 'state=RUNNING\n'
  printf 'startUtc=%s\n' "$(current_utc_iso)"
  printf 'branch=%s\n' "$EXPECTED_BRANCH"
  printf 'commit=%s\n' "$(git rev-parse HEAD)"
  printf 'hardTimeoutSeconds=%s\n' "$HARD_TIMEOUT_SECONDS"
  printf 'logFile=%s\n' "$LOG_FILE"
  printf 'finalReport=%s\n' "$FINAL_REPORT"
} > "$STATUS_FILE"

timeout \
  --signal=INT \
  --kill-after=60s \
  "${HARD_TIMEOUT_SECONDS}s" \
  codex \
    --strict-config \
    -c 'model_reasoning_effort="high"' \
    exec \
    --sandbox workspace-write \
    --output-last-message "$FINAL_REPORT" \
    - \
  < "$PROMPT_FILE" \
  > "$LOG_FILE" 2>&1 &

WATCHDOG_PID="$!"

while kill -0 "$WATCHDOG_PID" 2>/dev/null; do
  sleep 1

  elapsed_seconds="$(( $(current_epoch) - start_epoch ))"

  if [[ "$elapsed_seconds" -ge "$next_heartbeat_elapsed" ]] \
    && kill -0 "$WATCHDOG_PID" 2>/dev/null; then
    progress "Director still running. Elapsed: $(format_elapsed "$elapsed_seconds"). Log: $LOG_FILE"
    next_heartbeat_elapsed="$((next_heartbeat_elapsed + HEARTBEAT_SECONDS))"
  fi
done

set +e
wait "$WATCHDOG_PID"
director_exit="$?"
set -e

director_exit="$(effective_director_exit "$director_exit")"
WATCHDOG_PID=""
end_epoch="$(current_epoch)"
elapsed_seconds="$((end_epoch - start_epoch))"

case "$director_exit" in
  0)
    if ! (
      ensure_expected_branch
      ensure_expected_upstream
      ensure_clean_worktree
      verify_protected_refs
    ); then
      write_final_status "FINALIZATION_FAILED" "1" "$elapsed_seconds"

      warn "Director process exited successfully, but final safety checks failed."
      printf '\nRepository status after finalization failure:\n'
      git status --short --branch || true

      print_log_tail
      print_artifact_paths
      exit 1
    fi

    if ! final_report_is_present "$FINAL_REPORT"; then
      write_final_status "FINAL_REPORT_MISSING" "1" "$elapsed_seconds"

      warn "Director process exited successfully without a non-empty final report."
      printf '\nRepository status after missing final report:\n'
      git status --short --branch || true

      print_log_tail
      print_artifact_paths
      exit 1
    fi

    write_final_status "COMPLETED" "$director_exit" "$elapsed_seconds"

    progress "Director completed successfully in $(format_elapsed "$elapsed_seconds")."

    printf '\nDirector final report:\n'
    cat "$FINAL_REPORT"

    print_artifact_paths
    ;;

  124)
    write_final_status "HARD_TIMEOUT" "$director_exit" "$elapsed_seconds"

    warn "Director reached the hard watchdog timeout."
    warn "No automatic recovery or push will be attempted."

    printf '\nRepository status after timeout:\n'
    git status --short --branch || true

    print_log_tail
    print_artifact_paths
    exit 124
    ;;

  130)
    write_final_status "INTERRUPTED" "$director_exit" "$elapsed_seconds"

    warn "Director was interrupted."
    printf '\nRepository status after interruption:\n'
    git status --short --branch || true

    print_log_tail
    print_artifact_paths
    exit 130
    ;;

  *)
    write_final_status "FAILED" "$director_exit" "$elapsed_seconds"

    warn "Director failed with exit code $director_exit."
    printf '\nRepository status after failure:\n'
    git status --short --branch || true

    print_log_tail
    print_artifact_paths
    exit "$director_exit"
    ;;
esac
