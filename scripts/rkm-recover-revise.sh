#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TAIL_LINES="${TAIL_LINES:-80}"
REVIEW_CONTEXT_LINES="${REVIEW_CONTEXT_LINES:-180}"
CYCLE_OUTPUT="/tmp/rkm-cycle-output.txt"
RECOVER_OUTPUT="/tmp/rkm-recover-revise-output.txt"
REVIEW_OUTPUT="/tmp/rkm-recover-revise-review.txt"
PROMPT_FILE=""

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

cleanup() {
  if [[ -n "$PROMPT_FILE" && -f "$PROMPT_FILE" ]]; then
    rm -f "$PROMPT_FILE"
  fi
}

changed_files() {
  git status --short | while IFS= read -r status_line; do
    [[ -n "$status_line" ]] || continue
    printf '%s\n' "${status_line:3}"
  done
}

single_changed_file() {
  local count
  count="$(changed_files | sed '/^$/d' | wc -l | tr -d ' ')"

  if [[ "$count" == "0" ]]; then
    fail "Expected exactly one changed project file, found zero."
  fi

  if [[ "$count" != "1" ]]; then
    git status --short
    fail "Expected exactly one changed project file, found $count."
  fi

  changed_files | sed -n '1p'
}

ensure_project_file() {
  local file_path="$1"

  case "$file_path" in
    /*|../*|*/../*|.git/*|.agents/*|.codex/*)
      fail "Changed path is not an allowed project file: $file_path"
      ;;
  esac

  if [[ ! -e "$file_path" ]]; then
    fail "Changed file does not exist in the working tree: $file_path"
  fi
}

create_prompt() {
  local changed_file="$1"
  local recovery_context

  if [[ -f "$CYCLE_OUTPUT" ]]; then
    recovery_context="$(tail -n "$REVIEW_CONTEXT_LINES" "$CYCLE_OUTPUT")"
  else
    recovery_context="No prior Reviewer output was found at $CYCLE_OUTPUT."
  fi

  PROMPT_FILE="$(mktemp /tmp/rkm-recover-revise-prompt.XXXXXXXX)"

  cat >"$PROMPT_FILE" <<EOF
You are recovering an RKM single-file REVISE state.

Changed file:
$changed_file

Recovery context from the latest Reviewer output, if available (last $REVIEW_CONTEXT_LINES lines only):
$(printf '%s\n' "$recovery_context")

Task:
- Modify exactly this changed file: $changed_file
- Address the Reviewer REVISE issues from the recovery context.
- Preserve the rest of the file and repository behavior.
- Do not modify, create, delete, format, or normalize any other file.
- Do not commit.
- Run: bash scripts/validate-rkm.sh
- Report the validation command and result, the touched file, and final git status --short.
EOF
}

run_codex_recovery() {
  local prompt_content
  prompt_content="$(cat "$PROMPT_FILE")"
  codex exec --sandbox workspace-write "$prompt_content" >"$RECOVER_OUTPUT" 2>&1
}

run_reviewer() {
  local changed_file="$1"
  local review_prompt
  local status_before
  local status_after

  review_prompt="You are acting as Reviewer only. Review the current RKM git diff, focused on this changed file: $changed_file. Follow the Reviewer Protocol in AGENTS.md. Do not modify files. Return exactly one verdict: ACCEPT, REVISE, or STOP."
  status_before="$(git status --porcelain)"

  codex exec --sandbox read-only "$review_prompt" >"$REVIEW_OUTPUT" 2>&1

  status_after="$(git status --porcelain)"
  if [[ "$status_after" != "$status_before" ]]; then
    git status --short
    fail "Reviewer modified the working tree or index."
  fi
}

parse_verdict() {
  python3 scripts/rkm-review-verdict.py "$REVIEW_OUTPUT"
}

require_command codex
require_command git
require_command bash
require_command mktemp
require_command tail
require_command python3
require_command cat
require_command sed
require_command wc
require_command tr
require_command make

trap cleanup EXIT

changed_file="$(single_changed_file)"
ensure_project_file "$changed_file"
create_prompt "$changed_file"

if ! run_codex_recovery; then
  printf '\nCodex recovery output tail (%s lines):\n' "$TAIL_LINES"
  tail -n "$TAIL_LINES" "$RECOVER_OUTPUT"
  fail "Codex recovery failed."
fi

printf '\nCodex recovery output tail (%s lines):\n' "$TAIL_LINES"
tail -n "$TAIL_LINES" "$RECOVER_OUTPUT"

make validate

if ! run_reviewer "$changed_file"; then
  printf '\nReviewer output tail (%s lines):\n' "$TAIL_LINES"
  tail -n "$TAIL_LINES" "$REVIEW_OUTPUT"
  fail "Reviewer run failed."
fi

printf '\nReviewer output tail (%s lines):\n' "$TAIL_LINES"
tail -n "$TAIL_LINES" "$REVIEW_OUTPUT"

verdict="$(parse_verdict)"

case "$verdict" in
  ACCEPT)
    git add -- "$changed_file"
    git diff --cached --check
    git commit --no-verify -m "Recover ${changed_file}"
    git status --short
    ;;
  REVISE|STOP)
    git status --short
    fail "Reviewer returned $verdict. Leaving $changed_file uncommitted."
    ;;
  *)
    git status --short
    fail "Unexpected Reviewer verdict: $verdict"
    ;;
esac
