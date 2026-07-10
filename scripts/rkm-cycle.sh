#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TARGET_ACCEPTED_FILES="${1:-3}"
CREATOR_PROMPT="Create exactly one next missing RKM architecture or schema file that naturally follows from the current project state. Follow AGENTS.md strictly. Do not commit."
REVIEWER_PROMPT="You are acting as Reviewer only. Review the current RKM git diff. Follow the Reviewer Protocol in AGENTS.md. Do not modify files. Return ACCEPT, REVISE, or STOP."

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
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
  local verdict
  verdict="$(
    sed -nE \
      -e 's/^[[:space:]]*([-*]|•)?[[:space:]]*Verdict:[[:space:]]*(ACCEPT|REVISE|STOP)[[:space:]]*$/\2/p' \
      -e 's/^[[:space:]]*(ACCEPT|REVISE|STOP)[[:space:]]*$/\1/p' \
      "$output_file" | sed -n '1p'
  )"
  if [[ -z "$verdict" ]]; then
    cat "$output_file"
    fail "Reviewer did not return ACCEPT, REVISE or STOP."
  fi
  printf '%s' "$verdict"
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
  CREATOR_OUTPUT="$(new_temp_file)"
  codex exec --sandbox workspace-write "$CREATOR_PROMPT" | tee "$CREATOR_OUTPUT"
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

  REVIEWER_OUTPUT="$(new_temp_file)"
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

require_command codex
require_command git
require_command grep
require_command sed
require_command tee
require_command mktemp
require_command wc
require_command tr

if ! [[ "$TARGET_ACCEPTED_FILES" =~ ^[0-9]+$ ]] || [[ "$TARGET_ACCEPTED_FILES" -lt 1 ]]; then
  fail "Accepted file target must be a positive integer."
fi

trap cleanup EXIT
ensure_clean_worktree

accepted_files=0

while [[ "$accepted_files" -lt "$TARGET_ACCEPTED_FILES" ]]; do
  iteration=$((accepted_files + 1))
  printf '\nRKM cycle iteration %s of %s\n' "$iteration" "$TARGET_ACCEPTED_FILES"

  run_creator
  prepare_diff_for_review
  run_reviewer

  verdict="$(parse_verdict "$REVIEWER_OUTPUT")"
  printf '\nReviewer verdict: %s\n' "$verdict"

  if [[ "$verdict" == "REVISE" || "$verdict" == "STOP" ]]; then
    printf '\nReviewer output:\n'
    cat "$REVIEWER_OUTPUT"
    exit 1
  fi

  changed_file="$(single_changed_file)"

  if [[ "$changed_file" == "AGENTS.md" ]]; then
    fail "RKM cycle must never modify AGENTS.md."
  fi

  bash scripts/validate-rkm.sh

  git add -- "$changed_file"
  git diff --cached --check

  commit_message="$(commit_message_for_file "$changed_file")"
  git commit -m "$commit_message"

  accepted_files=$((accepted_files + 1))
done

printf '\nRKM cycle completed: %s accepted file(s) committed.\n' "$accepted_files"
git status --short
