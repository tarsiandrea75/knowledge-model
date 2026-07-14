#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ATTEMPTS="${1:-5}"
CREATOR_PROMPT="Create or modify exactly one project file for the next missing RKM architecture or schema item that naturally follows from the current project state. Follow AGENTS.md strictly. Do not infer that an architecture document is missing solely from a schema name, file name, or one-to-one schema-to-document comparison. Before creating a new architecture document, inspect existing architecture documents for semantic coverage of the proposed concept. Treat an existing canonical document as authoritative when it already covers the concept, even when its file name is not an exact match for a schema name. Do not create a parallel document by inventing distinctions such as concept model versus document-level contract unless that distinction is explicitly established in existing repository architecture or governance. Ground the selected work in a concrete repository need such as the governance backlog, rule coverage report, task guides, an explicit architectural gap, or a demonstrably uncovered schema contract. When a candidate is already covered semantically, reject that candidate and choose another genuinely missing item. Prefer no change over creating a speculative or duplicate architecture contract when no safe candidate can be demonstrated. Do not commit."
REVIEWER_PROMPT="You are acting as Reviewer only. Review the current RKM git diff. Follow the Reviewer Protocol in AGENTS.md. Do not modify files. Return ACCEPT, REVISE, or STOP."

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

progress() {
  printf '[rkm-discover] %s\n' "$1" >&2
}

now_seconds() {
  date +%s
}

elapsed_seconds() {
  local start="$1"
  local end
  end="$(now_seconds)"
  printf '%ss' "$((end - start))"
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

ensure_clean_main_worktree() {
  cd "$ROOT_DIR"
  if [[ -n "$(git status --porcelain)" ]]; then
    git status --short
    fail "Main working tree must be clean before starting RKM discovery."
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
    return 1
  fi

  changed_files | sed -n '1p'
}

parse_verdict() {
  local output_file="$1"
  local verdict
  verdict="$(
    sed -nE \
      -e 's/^[[:space:]]*([-*])?[[:space:]]*\*\*[[:space:]]*[Vv][Ee][Rr][Dd][Ii][Cc][Tt]:[[:space:]]*`?\**(ACCEPT|REVISE|STOP)\**`?[[:space:]]*\*\*[[:space:]]*$/\2/p' \
      -e 's/^[[:space:]]*([-*])?[[:space:]]*[Vv][Ee][Rr][Dd][Ii][Cc][Tt]:[[:space:]]*`?\**(ACCEPT|REVISE|STOP)\**`?[[:space:]]*$/\2/p' \
      -e 's/^[[:space:]]*\*\*[[:space:]]*(ACCEPT|REVISE|STOP)[[:space:]]*\*\*[[:space:]]*$/\1/p' \
      -e 's/^[[:space:]]*`?(ACCEPT|REVISE|STOP)`?[[:space:]]*$/\1/p' \
      "$output_file" | sed -n '1p'
  )"
  if [[ -z "$verdict" ]]; then
    return 1
  fi
  printf '%s' "$verdict"
}

prepare_diff_for_review() {
  local file_path="$1"
  if git status --porcelain -- "$file_path" | grep -q '^?? '; then
    git add -N -- "$file_path"
  fi
}

run_creator() {
  codex exec --sandbox workspace-write "$CREATOR_PROMPT"
}

run_validation() {
  bash scripts/validate-rkm.sh
}

is_codex_sandbox_runtime_init_error() {
  local output_file="$1"
  grep -Eiq \
    '((sandbox|runtime).*(init|initializ|start|startup|launch|create|setup))|((init|initializ|start|startup|launch|create|setup).*(sandbox|runtime))|Read-only file system|failed to initialize in-process app-server client|could not create PATH aliases|os error 30' \
    "$output_file"
}

run_reviewer_with_sandbox() {
  local sandbox="$1"
  local output_file="$2"

  codex exec --sandbox "$sandbox" "$REVIEWER_PROMPT" >>"$output_file" 2>&1
}

run_reviewer() {
  local output_file="$1"
  local status_before
  local status_after
  local reviewer_exit

  status_before="$(git status --porcelain)"

  : >"$output_file"
  if run_reviewer_with_sandbox read-only "$output_file"; then
    reviewer_exit=0
  else
    reviewer_exit="$?"
    if is_codex_sandbox_runtime_init_error "$output_file"; then
      printf '\nRetrying Reviewer with workspace-write sandbox after Codex sandbox/runtime initialization failure.\n' >>"$output_file"
      if run_reviewer_with_sandbox workspace-write "$output_file"; then
        reviewer_exit=0
      else
        reviewer_exit="$?"
      fi
    fi
  fi

  status_after="$(git status --porcelain)"

  if [[ "$status_after" != "$status_before" ]]; then
    git status --short
    return 2
  fi

  return "$reviewer_exit"
}

reset_discovery_worktree() {
  cd "$WORKTREE_DIR"
  git reset --hard HEAD >/dev/null
  git clean -fdx >/dev/null
}

save_attempt_artifacts() {
  local attempt_dir="$1"

  git status --short >"$attempt_dir/git-status.txt"
  git diff --binary >"$attempt_dir/diff.patch"
}

cleanup() {
  cd "$ROOT_DIR"
  if [[ -n "${WORKTREE_DIR:-}" && -d "$WORKTREE_DIR" ]]; then
    git worktree remove --force "$WORKTREE_DIR" >/dev/null 2>&1 || true
  fi
}

require_command codex
require_command date
require_command git
require_command grep
require_command mktemp
require_command sed
require_command tee
require_command tr
require_command wc

if ! [[ "$ATTEMPTS" =~ ^[0-9]+$ ]] || [[ "$ATTEMPTS" -lt 1 ]]; then
  fail "Discovery attempts must be a positive integer."
fi

total_start="$(now_seconds)"

ensure_clean_main_worktree

REPORT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/rkm-discovery-report-XXXXXXXX")"
WORKTREE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/rkm-discovery-XXXXXXXX")"
rmdir "$WORKTREE_DIR"
trap cleanup EXIT

worktree_start="$(now_seconds)"
progress "Preparing discovery worktree."
git worktree add --detach "$WORKTREE_DIR" HEAD >/dev/null
progress "Preparing discovery worktree completed in $(elapsed_seconds "$worktree_start")."

accept_count=0
revise_count=0
stop_count=0
validator_failure_count=0
other_error_count=0
gap_count=0

progress "Report directory: $REPORT_DIR"
progress "Discovery worktree: $WORKTREE_DIR"

for attempt in $(seq 1 "$ATTEMPTS"); do
  attempt_start="$(now_seconds)"
  attempt_dir="$REPORT_DIR/attempt-$attempt"
  mkdir -p "$attempt_dir"
  progress "Attempt $attempt of $ATTEMPTS started."

  phase_start="$(now_seconds)"
  progress "Attempt $attempt: preparing worktree."
  reset_discovery_worktree
  progress "Attempt $attempt: preparing worktree completed in $(elapsed_seconds "$phase_start")."

  cd "$WORKTREE_DIR"
  phase_start="$(now_seconds)"
  progress "Attempt $attempt: Creator run started."
  set +e
  run_creator >"$attempt_dir/creator-output.txt" 2>&1
  creator_status="$?"
  set -e
  progress "Attempt $attempt: Creator run completed in $(elapsed_seconds "$phase_start") with exit status $creator_status."

  if [[ "$creator_status" -ne 0 ]]; then
    git status --short >"$attempt_dir/git-status.txt"
    git diff --binary >"$attempt_dir/diff.patch"
    printf 'Creator failed with exit status %s.\n' "$creator_status" >"$attempt_dir/error.txt"
    other_error_count=$((other_error_count + 1))
    progress "Attempt $attempt ended with Creator error after $(elapsed_seconds "$attempt_start")."
    continue
  fi

  if ! candidate_file="$(single_changed_file)"; then
    git status --short >"$attempt_dir/git-status.txt"
    git diff --binary >"$attempt_dir/diff.patch"
    printf 'Expected exactly one changed candidate file, found %s.\n' "$(changed_file_count)" >"$attempt_dir/error.txt"
    other_error_count=$((other_error_count + 1))
    progress "Attempt $attempt ended without exactly one changed file after $(elapsed_seconds "$attempt_start")."
    continue
  fi

  prepare_diff_for_review "$candidate_file"

  phase_start="$(now_seconds)"
  progress "Attempt $attempt: validation started."
  set +e
  run_validation >"$attempt_dir/validator-output.txt" 2>&1
  validator_status="$?"
  set -e
  progress "Attempt $attempt: validation completed in $(elapsed_seconds "$phase_start") with exit status $validator_status."
  if [[ "$validator_status" -ne 0 ]]; then
    validator_failure_count=$((validator_failure_count + 1))
  fi

  phase_start="$(now_seconds)"
  progress "Attempt $attempt: Reviewer run started."
  set +e
  run_reviewer "$attempt_dir/reviewer-output.txt"
  reviewer_status="$?"
  set -e
  progress "Attempt $attempt: Reviewer run completed in $(elapsed_seconds "$phase_start") with exit status $reviewer_status."

  if [[ "$reviewer_status" -ne 0 ]]; then
    printf 'Reviewer failed with exit status %s.\n' "$reviewer_status" >"$attempt_dir/error.txt"
    other_error_count=$((other_error_count + 1))
    save_attempt_artifacts "$attempt_dir"
    progress "Attempt $attempt ended with Reviewer error after $(elapsed_seconds "$attempt_start")."
    continue
  fi

  if ! verdict="$(parse_verdict "$attempt_dir/reviewer-output.txt")"; then
    printf 'Reviewer did not return ACCEPT, REVISE or STOP.\n' >"$attempt_dir/error.txt"
    other_error_count=$((other_error_count + 1))
    save_attempt_artifacts "$attempt_dir"
    progress "Attempt $attempt ended with unparsable Reviewer verdict after $(elapsed_seconds "$attempt_start")."
    continue
  fi

  printf '%s\n' "$verdict" >"$attempt_dir/verdict.txt"

  case "$verdict" in
    ACCEPT)
      accept_count=$((accept_count + 1))
      ;;
    REVISE)
      revise_count=$((revise_count + 1))
      ;;
    STOP)
      stop_count=$((stop_count + 1))
      ;;
  esac

  if [[ "$validator_status" -eq 0 && ( "$verdict" == "REVISE" || "$verdict" == "STOP" ) ]]; then
    printf 'Validation passed but Reviewer returned %s. This may indicate a validator or instruction gap.\n' "$verdict" >"$attempt_dir/possible-gap.txt"
    gap_count=$((gap_count + 1))
  fi

  save_attempt_artifacts "$attempt_dir"
  progress "Attempt $attempt ended with verdict $verdict after $(elapsed_seconds "$attempt_start")."
done

summary_start="$(now_seconds)"
progress "Summary started."
cd "$ROOT_DIR"
ensure_clean_main_worktree

printf '\nRKM discovery summary\n'
printf 'ACCEPT: %s\n' "$accept_count"
printf 'REVISE: %s\n' "$revise_count"
printf 'STOP: %s\n' "$stop_count"
printf 'Validator failures: %s\n' "$validator_failure_count"
printf 'Other errors: %s\n' "$other_error_count"
printf 'Possible validator or instruction gaps: %s\n' "$gap_count"
printf 'Report directory: %s\n' "$REPORT_DIR"
progress "Summary completed in $(elapsed_seconds "$summary_start")."
progress "Total discovery run completed in $(elapsed_seconds "$total_start")."
