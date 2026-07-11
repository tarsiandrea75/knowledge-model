#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TAIL_LINES="${TAIL_LINES:-80}"
PROMPT_FILE=""
TARGET_FILE=""
COMMIT_MESSAGE=""
CODEX_OUTPUT=""

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

usage() {
  printf 'Usage: %s --prompt-file PATH --file PATH --message TEXT\n' "${0##*/}" >&2
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

print_codex_output_tail() {
  if [[ -n "$CODEX_OUTPUT" && -f "$CODEX_OUTPUT" ]]; then
    printf '\nCodex output tail (%s lines):\n' "$TAIL_LINES" >&2
    tail -n "$TAIL_LINES" "$CODEX_OUTPUT" >&2
  fi
}

on_error() {
  local exit_code="$?"
  print_codex_output_tail
  exit "$exit_code"
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --prompt-file)
      [[ "$#" -ge 2 ]] || fail "Missing value for --prompt-file."
      PROMPT_FILE="$2"
      shift 2
      ;;
    --file)
      [[ "$#" -ge 2 ]] || fail "Missing value for --file."
      TARGET_FILE="$2"
      shift 2
      ;;
    --message)
      [[ "$#" -ge 2 ]] || fail "Missing value for --message."
      COMMIT_MESSAGE="$2"
      shift 2
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

if [[ -z "$PROMPT_FILE" ]]; then
  usage
  fail "Missing required argument: --prompt-file."
fi

if [[ -z "$TARGET_FILE" ]]; then
  usage
  fail "Missing required argument: --file."
fi

if [[ -z "$COMMIT_MESSAGE" ]]; then
  usage
  fail "Missing required argument: --message."
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  fail "Prompt file does not exist: $PROMPT_FILE"
fi

require_command codex
require_command git
require_command make
require_command mktemp
require_command tail

CODEX_OUTPUT="$(mktemp /tmp/rkm-codex-commit.XXXXXXXX)"
trap on_error ERR

prompt_content="$(cat "$PROMPT_FILE")"

set +e
codex exec --sandbox workspace-write "$prompt_content" >"$CODEX_OUTPUT" 2>&1
codex_status="$?"
set -e

if [[ "$codex_status" -ne 0 ]]; then
  print_codex_output_tail
  exit "$codex_status"
fi

printf '\nCodex output tail (%s lines):\n' "$TAIL_LINES"
tail -n "$TAIL_LINES" "$CODEX_OUTPUT"

make validate
git add -- "$TARGET_FILE"
git diff --cached --check
git commit -m "$COMMIT_MESSAGE"
git status --short
