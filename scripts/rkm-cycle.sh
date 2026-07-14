#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TARGET_ACCEPTED_FILES="${1:-3}"
CREATOR_PROMPT="Create or modify exactly one project file for the next missing RKM architecture or schema item that naturally follows from the current project state. Follow AGENTS.md strictly. Do not infer that an architecture document is missing solely from a schema name, file name, or one-to-one schema-to-document comparison. Before creating a new architecture document, inspect existing architecture documents for semantic coverage of the proposed concept. Treat an existing canonical document as authoritative when it already covers the concept, even when its file name is not an exact match for a schema name. Do not create a parallel document by inventing distinctions such as concept model versus document-level contract unless that distinction is explicitly established in existing repository architecture or governance. Ground the selected work in a concrete repository need such as the governance backlog, rule coverage report, task guides, an explicit architectural gap, or a demonstrably uncovered schema contract. When a candidate is already covered semantically, reject that candidate and choose another genuinely missing item. Prefer no change over creating a speculative or duplicate architecture contract when no safe candidate can be demonstrated. Ensure exactly one final newline and no blank line at EOF. Do not commit."
REVIEWER_PROMPT="You are acting as Reviewer only. Review the current RKM git diff. Follow the Reviewer Protocol in AGENTS.md. Do not modify files. Return ACCEPT, REVISE, or STOP."

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

progress() {
  printf '[rkm-cycle] %s\n' "$1" >&2
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

clear_spinner_line() {
  printf '\r%*s\r' 100 '' >&2
}

run_with_spinner() {
  local label="$1"
  shift

  local start_epoch
  local end_epoch
  local command_status
  local spinner_index=0
  local spinner_frames=('|' '/' '-' '\')
  local command_pid

  start_epoch="$(current_epoch)"
  progress "$label started at $(current_time)."

  "$@" &
  command_pid="$!"

  while kill -0 "$command_pid" 2>/dev/null; do
    printf '\r[rkm-cycle] %s %s running' "${spinner_frames[$spinner_index]}" "$label" >&2
    spinner_index=$(((spinner_index + 1) % ${#spinner_frames[@]}))
    sleep 0.2
  done

  set +e
  wait "$command_pid"
  command_status="$?"
  set -e

  clear_spinner_line
  end_epoch="$(current_epoch)"
  progress "$label ended at $(current_time). Elapsed: $(format_elapsed "$((end_epoch - start_epoch))")."

  return "$command_status"
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

new_temp_file() {
  mktemp "${TMPDIR:-/tmp}/rkm-cycle.XXXXXX"
}

cleanup() {
  if [[ -n "${CREATOR_OUTPUT:-}" && -f "$CREATOR_OUTPUT" ]]; then
    rm -f "$CREATOR_OUTPUT"
  fi
  if [[ -n "${REVIEWER_OUTPUT:-}" && -f "$REVIEWER_OUTPUT" ]]; then
    rm -f "$REVIEWER_OUTPUT"
  fi
}

ensure_clean_worktree() {
  if [[ -n "$(git status --porcelain)" ]]; then
    git status --short
    fail "Working tree must be clean before starting the RKM cycle."
  fi
}

changed_files() {
  git status --porcelain | sed -E 's/^.. //'
}

changed_file_count() {
  changed_files | sed '/^$/d' | wc -l | tr -d ' '
}

single_changed_file() {
  local count
  count="$(changed_file_count)"
  if [[ "$count" != "1" ]]; then
    git status --short
    fail "Expected exactly one changed project file, found $count."
  fi

  changed_files | sed -n '1p'
}

parse_verdict() {
  local output_file="$1"
  local parser_output

  if ! parser_output="$(python3 scripts/rkm-review-verdict.py "$output_file")"; then
    cat "$output_file"
    fail "Reviewer verdict parser could not find ACCEPT, REVISE or STOP."
  fi

  printf '%s' "$parser_output"
}

prepare_diff_for_review() {
  local file_path
  file_path="$(single_changed_file)"

  if git status --porcelain -- "$file_path" | grep -q '^?? '; then
    IS_NEW_FILE=1
    git add -N -- "$file_path"
  else
    IS_NEW_FILE=0
  fi
}

commit_message_for_file() {
  local file_path="$1"
  local action="Update"
  local subject="$file_path"

  if [[ "${IS_NEW_FILE:-0}" == "1" ]]; then
    action="Add"
  fi

  if [[ "$file_path" == schema/*.schema.json ]]; then
    subject="${file_path#schema/}"
    subject="${subject%.schema.json}"
    subject="${subject//-/ } schema"
  fi

  printf '%s %s' "$action" "$subject"
}

run_creator() {
  codex exec --sandbox workspace-write "$CREATOR_PROMPT" 2>&1 | tee "$CREATOR_OUTPUT"
}

is_codex_sandbox_runtime_init_error() {
  local output_file="$1"
  grep -Eiq \
    '((sandbox|runtime).*(init|initializ|start|startup|launch|create|setup))|((init|initializ|start|startup|launch|create|setup).*(sandbox|runtime))|Read-only file system|failed to initialize in-process app-server client|could not create PATH aliases|os error 30' \
    "$output_file"
}

run_reviewer_with_sandbox() {
  local sandbox="$1"
  codex exec --sandbox "$sandbox" "$REVIEWER_PROMPT" 2>&1 | tee "$REVIEWER_OUTPUT"
}

run_reviewer() {
  local reviewer_status_before
  local reviewer_status_after
  local reviewer_exit

  reviewer_status_before="$(git status --porcelain)"

  if run_reviewer_with_sandbox read-only; then
    reviewer_exit=0
  else
    reviewer_exit=$?
    if is_codex_sandbox_runtime_init_error "$REVIEWER_OUTPUT"; then
      : >"$REVIEWER_OUTPUT"
      printf '\nRetrying Reviewer with workspace-write sandbox after Codex sandbox/runtime initialization failure.\n'
      if run_reviewer_with_sandbox workspace-write; then
        reviewer_exit=0
      else
        reviewer_exit=$?
      fi
    fi
  fi

  reviewer_status_after="$(git status --porcelain)"
  if [[ "$reviewer_status_after" != "$reviewer_status_before" ]]; then
    git status --short
    fail "Reviewer modified the working tree or index."
  fi

  return "$reviewer_exit"
}

run_validation() {
  bash scripts/validate-rkm.sh
}

run_commit() {
  local changed_file="$1"
  local commit_message="$2"

  git add -- "$changed_file"
  git diff --cached --check
  git commit --no-verify -m "$commit_message"
}

require_command codex
require_command date
require_command git
require_command grep
require_command sed
require_command sleep
require_command tee
require_command mktemp
require_command python3
require_command wc
require_command tr

if ! [[ "$TARGET_ACCEPTED_FILES" =~ ^[0-9]+$ ]] || [[ "$TARGET_ACCEPTED_FILES" -lt 1 ]]; then
  fail "Accepted file target must be a positive integer."
fi

trap cleanup EXIT
ensure_clean_worktree

accepted_files=0
cycle_start_epoch="$(current_epoch)"
progress "Cycle started at $(current_time)."

while [[ "$accepted_files" -lt "$TARGET_ACCEPTED_FILES" ]]; do
  iteration=$((accepted_files + 1))
  iteration_start_epoch="$(current_epoch)"
  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES started at $(current_time)."

  CREATOR_OUTPUT="$(new_temp_file)"
  run_with_spinner "Creator" run_creator
  prepare_diff_for_review

  REVIEWER_OUTPUT="$(new_temp_file)"
  run_with_spinner "Reviewer" run_reviewer

  verdict="$(parse_verdict "$REVIEWER_OUTPUT")"
  progress "Reviewer verdict parsed: $verdict."

  if [[ "$verdict" == "REVISE" || "$verdict" == "STOP" ]]; then
    progress "Reviewer requested $verdict; printing Reviewer output before stopping."
    printf '\nReviewer output:\n'
    cat "$REVIEWER_OUTPUT"
    exit 1
  fi

  changed_file="$(single_changed_file)"

  if [[ "$changed_file" == "AGENTS.md" ]]; then
    fail "RKM cycle must never modify AGENTS.md."
  fi

  run_with_spinner "validation" run_validation

  progress "Preparing commit for $changed_file."
  commit_message="$(commit_message_for_file "$changed_file")"
  run_with_spinner "commit" run_commit "$changed_file" "$commit_message"
  progress "Commit completed: $commit_message."

  accepted_files=$((accepted_files + 1))
  iteration_end_epoch="$(current_epoch)"
  progress "Iteration $iteration of $TARGET_ACCEPTED_FILES ended at $(current_time). Elapsed: $(format_elapsed "$((iteration_end_epoch - iteration_start_epoch))")."
done

cycle_end_epoch="$(current_epoch)"
progress "Cycle ended at $(current_time). Elapsed: $(format_elapsed "$((cycle_end_epoch - cycle_start_epoch))")."
progress "Cycle completed: $accepted_files accepted file(s) committed."
git status --short
